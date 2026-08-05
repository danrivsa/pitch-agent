import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from langchain.messages import HumanMessage
from pydantic import BaseModel
from dotenv import load_dotenv
from agent.pitch_agent import get_running_agent, _get_config

load_dotenv()
agent_executor = get_running_agent()


app = FastAPI()
origins  = [
    os.environ["PORTFOLIO_URL"]
]

print(f"Allowing CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatPayload(BaseModel):
    message: str
    thread_id: str = None 

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/chat/stream")
async def stream_chat_api(payload: ChatPayload):
    print(f"Received message: {payload.message} with thread_id: {payload.thread_id}")
    
    async def sse_generator():
        try:
            
            # Start streaming raw LangChain execution events
            async for event in agent_executor.astream_events(
                {
                    "messages": [HumanMessage(content=payload.message)],
                },
                version="v2",
                config=_get_config(payload.thread_id)
            ):
                kind = event["event"]
                
                # 1. TEXT TOKENS STREAMING
                if kind == "on_chat_model_stream":
                    chunk = event["data"]["chunk"]
                    # Reasoning tokens come through additional_kwargs (e.g. Groq's
                    # reasoning_format="parsed" streams them as reasoning_content)
                    reasoning = chunk.additional_kwargs.get("reasoning_content")
                    # Google Gemini 3 streams reasoning as thinking/reasoning content
                    # blocks inside chunk.content instead
                    if not reasoning and isinstance(chunk.content, list):
                        thinking = [
                            b.get("thinking") or b.get("reasoning")
                            for b in chunk.content
                            if isinstance(b, dict)
                            and b.get("type") in ("thinking", "reasoning")
                        ]
                        reasoning = "".join(thinking)
                    if reasoning:
                        yield f"event: reasoning\ndata: {json.dumps({'text': reasoning})}\n\n"
                    # Standard text tokens
                    elif chunk.content:
                        if isinstance(chunk.content, list):
                            text = "".join(
                                b.get("text", "")
                                for b in chunk.content
                                if isinstance(b, dict) and b.get("type") == "text"
                            )
                        else:
                            text = chunk.content
                        yield f"event: message\ndata: {json.dumps({'text': text})}\n\n"

                # 2. TOOL CALL DETECTED (Agent decided to open your resume/bio file)
                elif kind == "on_tool_start":
                    tool_info = {"name": event["name"], "input": event["data"].get("input")}
                    yield f"event: tool_start\ndata: {json.dumps(tool_info)}\n\n"

                # 3. TOOL OUTPUT RECEIVED
                elif kind == "on_tool_end":
                    yield f"event: tool_end\ndata: {json.dumps({'name': event['name']})}\n\n"
        except Exception as e:
            # This logs the real issue to FastAPI terminal!
            print(f"STREAM ERROR DETECTED: {str(e)}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    # Return a continuous streaming text response formatted as text/event-stream
    return StreamingResponse(sse_generator(), media_type="text/event-stream")


@app.options("/api/chat/stream")
async def chat_stream_options(request: Request):
    # Lightweight handler for CORS preflight requests — helps avoid 400s behind proxies
    print(f"Request: {request}")
    print(f"Preflight OPTIONS for /api/chat/stream from: {request.client} headers: {dict(request.headers)}")
    return Response(status_code=200)