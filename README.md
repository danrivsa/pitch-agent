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

## Running the FastAPI Server

Start the API server with Uvicorn:

```bash
uv run uvicorn api.api:app --host 0.0.0.0 --port 3000 --reload
```

The chat streaming endpoint is:

```text
POST /api/chat/stream
```

## Request Format

The endpoint expects a JSON payload with a required `message` field:

```json
{
	"message": "Can you summarize Daniel's backend experience?"
}
```

Example `curl` request:

```bash
curl -N -X POST "http://localhost:3000/api/chat/stream" \
	-H "Content-Type: application/json" \
	-H "Accept: text/event-stream" \
	-d '{"message":"Can you summarize Daniel\'s backend experience?"}'
```

The response is streamed as Server-Sent Events (`text/event-stream`) with events such as `message`, `reasoning`, `tool_start`, `tool_end`, and `error`.
