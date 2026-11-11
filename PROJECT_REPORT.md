# AI Chat Application — Project Report

## Objective

To develop a simple AI-powered chat application using Python and an LLM API. The application accepts user input, sends it securely to a language model, displays the generated response, maintains conversation history, supports custom instructions, and monitors token usage.

## Learning outcomes covered

### 1. LLM APIs, authentication, environment variables, and Python integration

The project uses the OpenAI Python SDK. Authentication is performed with an API key stored in a `.env` file and loaded through `python-dotenv`. The key is not hard-coded into the Python source code.

### 2. Conversation management and token optimization

The application stores user and assistant messages in Streamlit session state. It sends previous messages to the model when conversation history is enabled. The sidebar allows the user to set model, temperature, and maximum output tokens. These settings help control response creativity, response length, and token consumption.

### 3. Structured responses, error handling, and cost management

The app includes an optional JSON response mode. It handles missing credentials, rate limits, network errors, API status errors, and unexpected failures. It reads input/output token usage from the API response and calculates an approximate cost using configurable sample pricing values.

### 4. AI Chat Application

The Streamlit interface provides a chat input, chat bubbles, conversation history, custom instructions, model controls, JSON mode, usage metrics, and a clear-history button.

## Tools and technologies

| Technology | Purpose |
|---|---|
| Python | Application logic |
| OpenAI Python SDK | Connect to the LLM API |
| OpenAI Responses API | Generate model responses |
| Streamlit | Build the web user interface |
| python-dotenv | Load environment variables |
| JSON | Structured response format |

## Result

A functional browser-based AI chat application is provided. Users can submit prompts, receive model-generated answers, continue a conversation with context, customize assistant behavior, request JSON output, and view token usage with an approximate API cost.

## Conclusion

The project demonstrates the core workflow of an LLM-powered application: secure authentication, prompt and conversation construction, API communication, response display, error handling, and basic usage monitoring. It can be extended with user accounts, a database, file uploads, voice input, and deployment to a cloud platform.
