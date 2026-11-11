# AI Chat Application

A beginner-friendly Python + Streamlit chatbot using the OpenAI Responses API.

## Features

- Secure API authentication through environment variables
- Chat interface with user and assistant messages
- Conversation history during the current session
- Custom system-style instructions
- Model, temperature, and output-token controls
- Optional JSON-formatted response mode
- API error handling for missing keys, connection failures, rate limits, and API errors
- Input/output token tracking and approximate cost estimation
- Clear conversation button

## 1. Requirements

- Python 3.10+
- An OpenAI API key with API access and billing configured
- Internet connection

## 2. Setup

### Windows PowerShell

```powershell
mkdir ai-chat-application
cd ai-chat-application
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder with your API key:

```env
OPENAI_API_KEY=your_actual_api_key
OPENAI_MODEL=gpt-4.1-mini
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your API key.

## 3. Run

```bash
streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open it in your browser.

## 4. How it works

1. `python-dotenv` loads environment variables from `.env`.
2. The OpenAI client authenticates using `OPENAI_API_KEY`.
3. Streamlit captures the user's prompt.
4. The app sends the system-style instructions and conversation messages to the Responses API.
5. The response is displayed and saved in `st.session_state`.
6. Usage data is read from the API response and accumulated for the current session.
7. The cost estimate uses the sample rates in `app.py`; update these rates to match current provider pricing.

## 5. Message roles

- **System/developer-style instructions:** define the assistant's behavior. In this app, these are passed using the API's `instructions` field.
- **User:** the prompt sent by the person using the app.
- **Assistant:** the model's response.

## 6. Token and cost management

- Use a smaller model for routine questions.
- Keep the conversation history relevant; long histories consume more input tokens.
- Set a sensible maximum output token count.
- Use concise custom instructions.
- Track usage in the provider dashboard.
- The displayed cost is an estimate, not an invoice. Model prices can change.

## 7. Structured output

Enable **Request a JSON response** in the sidebar. The app requests JSON-formatted output. For production applications, validate the returned JSON against a schema before using it in another system.

## 8. Error handling

The app handles:
- Missing API key
- API rate limit or quota errors
- Network connection errors
- HTTP/API status errors
- Unexpected application errors

Never print or expose your API key in the interface or source code.

## 9. Project flow

```text
User opens Streamlit UI
        |
        v
Enters prompt + optional settings
        |
        v
Python reads API key from environment
        |
        v
Build instructions + chat history
        |
        v
Call LLM Responses API
        |
        v
Handle API response / errors
        |
        v
Display answer and save chat history
        |
        v
Track token usage and estimated cost
```

## 10. Suggested test cases

1. Send a normal question and verify the assistant responds.
2. Ask a follow-up question and verify the previous context is considered.
3. Change custom instructions and check the response style.
4. Enable JSON mode and ask for a JSON object.
5. Temporarily remove the API key and verify the missing-key message.
6. Enter an invalid model name in the environment and verify API error handling.
7. Clear the conversation and verify the history and usage counters reset.

## 11. Limitations and production improvements

- History is held in Streamlit session state; it is not permanent across all sessions.
- Cost rates are examples and must be checked against current official pricing.
- Add authentication, persistent database storage, rate limiting per user, moderation, schema validation, and deployment secrets before public production use.
