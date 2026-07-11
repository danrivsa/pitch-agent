# Pitch Agent

An AI agent that acts as a professional representative for Daniel Rivero, a Software/AI Engineer. It answers questions from recruiters, potential clients, and peers about his background, skills, and projects by loading contextual knowledge from skill files.

## How It Works

The agent uses LangChain to power an interactive conversation. It supports two model providers out of the box:

- **Google Generative AI** (default) — uses Gemini models.
- **Groq** — uses Groq's fast inference for models like `openai/gpt-oss-120b`.

When asked about specific topics, the agent loads relevant skills (e.g., resume data) into context to provide accurate, grounded answers—never guessing or hallucinating facts.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- A Google Generative AI API key or a Groq API key, depending on your chosen provider.

## Setup

1. Clone the repository and install dependencies:

```bash
uv sync
```

2. Create a `.env` file in the project root with your API key(s):

```
# Required for Google provider (default)
GEMINI_API_KEY=your_gemini_api_key_here

# Required for Groq provider
GROQ_API_KEY=your_groq_api_key_here

# Optional: set the provider (defaults to "google")
PITCH_AGENT_MODEL_PROVIDER=google  # or "groq"
```

## Running

```bash
uv run main.py
```

Type your message at the prompt. Type `exit` to quit.
