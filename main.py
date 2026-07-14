import asyncio

from langchain.messages import HumanMessage
from agent.pitch_agent import get_running_agent, get_config
from utils.logger import log_agent, log_reasoning, log_runtime, log_tool

async def main():
    
    config = get_config()
    agent = get_running_agent()
    thread_id = config["configurable"]["thread_id"]
    log_runtime(f"Agent is running with thread ID: {thread_id}")

    while True:
        user_input = await asyncio.to_thread(input, "User: ")
        if user_input.lower() == "exit":
            break

        stream = await agent.astream_events(
            {
                "messages": [
                    HumanMessage(content=user_input)
                ],
            },
            config=config,
            version='v3'
        )
        
        async def consume_messages(stream):
            async for message in stream.messages:
                log_reasoning(await message.reasoning)
                log_agent(await message.text)
                
        async def consume_tool_calls(stream):
            async for call in stream.tool_calls:
                log_tool(f"Tool call: {call.tool_name} with input: {call.input}")
                
        await asyncio.gather(consume_messages(stream), consume_tool_calls(stream))
                


if __name__ == "__main__":
    asyncio.run(main())
