import os
from dotenv import load_dotenv
from utils.logger import log_config, log_info, log_error

load_dotenv()  # Load environment variables from .env file

def get_langchain_available_models(provider_key: str):
    """
    Fetches the live list of model strings that you can pass into 
    LangChain's init_chat_model() or provider classes.
    """
    pk = provider_key.lower().strip()
    log_info(f"=== Fetching models compatible with LangChain provider: '{pk}' ===\n")

    # 1. GOOGLE (langchain-google-genai / google_genai)
    if pk in ["google", "google_genai"]:
        from google import genai
        if not os.environ.get("GEMINI_API_KEY"):
            log_error("Error: Please set the GEMINI_API_KEY environment variable.")
            return
        try:
            # LangChain's google-genai integration relies on the Google GenAI SDK
            client = genai.Client()
            for m in client.models.list():
                log_info(f"  - {m.name}")
        except Exception as e:
            log_error(f"Error fetching from Google: {e}")

    # 2. GROQ (langchain-groq / groq)
    elif pk == "groq":
        if not os.environ.get("GROQ_API_KEY"):
            log_error("Error: Please set the GROQ_API_KEY environment variable.")
            return
        try:
            from groq import Groq
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            models = client.models.list()
            for m in models.data:
                log_info(f"  - {m.id}")
        except Exception as e:
            log_error(f"Error fetching from Groq: {e}")
    else:
        log_error(f"Unknown or unmapped provider: '{provider_key}'")
        
def get_agent_model():
    """
    Returns the agent model based on the provider name (key).
    """
    # init provider key from environment variable 
    pk = os.environ.get("PITCH_AGENT_MODEL_PROVIDER", "google")
    
    if pk in ["google", "google_genai"]:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0,
            max_tokens=None,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2,
            # other params...
        )
    elif pk == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0,
            reasoning_effort="medium",
            max_tokens=None,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2,
            # other params...
        )
    else:
        log_error(f"Unknown or unmapped provider: '{pk}'")
        return None

if __name__ == "__main__":
    supported_providers = ["google", "groq"]
    while True:
        user_input = input(f"Enter a provider name to fetch models (supported providers {supported_providers}, or 'exit' to quit): ")
        if user_input.lower() not in supported_providers and user_input.lower() != 'exit':
            log_error(f"Unsupported provider '{user_input}'. Supported providers are: {supported_providers}")
            continue
        if user_input.lower() == 'exit':
            break
        get_langchain_available_models(user_input)
