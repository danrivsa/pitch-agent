import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain.messages import HumanMessage
from pydantic import BaseModel
from dotenv import load_dotenv
from agent.pitch_agent import get_running_agent, _get_config

load_dotenv()
agent_executor = get_running_agent()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("PORTFOLIO_URL","http://localhost:3000")],
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
                    content = event["data"]["chunk"].content
                    # Check for reasoning tokens if using a reasoning model (like deep thinking models)
                    # Some models put thoughts in a separate property, others use a standard chunk
                    metadata = event["data"]["chunk"].response_metadata
                    
                    # If the provider flags it explicitly as reasoning/thinking
                    if "reasoning_content" in metadata or "reasoning" in metadata:
                        reasoning_chunk = metadata.get("reasoning_content") or metadata.get("reasoning")
                        yield f"event: reasoning\ndata: {json.dumps({'text': reasoning_chunk})}\n\n"
                    
                    # Standard text tokens
                    elif content:
                        yield f"event: message\ndata: {json.dumps({'text': content})}\n\n"

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