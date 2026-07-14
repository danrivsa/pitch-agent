from email import message
import json

from tools.load_skill import load_skill
from utils.logger import log_config, log_runtime, log_info, log_error, log_agent,log_reasoning, log_tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from utils.models import get_agent_model
from middlewares.skill_middleware import SkillMiddleware
from langchain_core.utils.uuid import uuid7
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import asyncio

def _get_system_prompt() -> str:
    return """
You are the official AI representative for Daniel Rivero, a Software / AI Engineer.
Your goal is to answer questions from recruiters, potential clients, and peers about his background, skills, and projects.

# Core Directives:
1. Be professional, concise, and polite. You are an AI representing Daniel—do not pretend to *be* Daniel. Use third-person pronouns ("Daniel built...", "He graduated...").
2. Conversational bypass: If the user simply says "Hello" or asks "How are you?", answer naturally and warmly.
3. Information retrieval: If asked about a skill or project, call your tool, read the context, and summarize the relevant facts clearly.
4. The Hallucination Rule: If the user asks a question and the answer is NOT in your context (e.g., "What is his exact salary expectation?" or "Can he code in Rust?"), DO NOT guess or invent facts. 
5. Fallback response: If you don't know the answer, say exactly: "I don't have that specific information in my files, but Daniel would be happy to discuss that with you! You can reach out to him directly to schedule a meeting through the following channels: \n\n  - LinkedIn: <insert profile link>\n- Email: <insert email address>\n- GitHub: <insert GitHub link>\n\nHe looks forward to connecting with you!"

Always stick to these directives.
"""

def _generate_thread_id() -> str:
    return str(uuid7())

def _get_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}

def get_config() -> dict:
    thread_id = _generate_thread_id()
    config = _get_config(thread_id)
    return config

def get_running_agent():
    system_prompt = _get_system_prompt()
    tools = [load_skill]
    
    agent = create_agent(
        checkpointer= InMemorySaver(),
        model=get_agent_model(),
        system_prompt=system_prompt,
        middleware=[SkillMiddleware()],
        tools=tools
    )
    
    return agent