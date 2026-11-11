import json
import os
import time
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError

load_dotenv()

st.set_page_config(page_title="AI Chat Application", page_icon="🤖", layout="wide")

MODEL_DEFAULT = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
MODEL_PRICING = {
    # Illustrative USD prices per 1M tokens. Update from the provider's pricing page.
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to your .env file and restart the app."
        )
    return OpenAI(api_key=api_key, timeout=45.0, max_retries=2)

def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float | None:
    rates = MODEL_PRICING.get(model)
    if not rates:
        return None
    return (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000

def response_text(response: Any) -> str:
    # The SDK exposes output_text as a convenient aggregate for Responses API output.
    text_value = getattr(response, "output_text", "")
    if text_value:
        return text_value
    return "The model returned no text. Please try again."

if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_input_tokens" not in st.session_state:
    st.session_state.total_input_tokens = 0
if "total_output_tokens" not in st.session_state:
    st.session_state.total_output_tokens = 0

st.title("🤖 AI Chat Application")
st.caption("Python • LLM API • Conversation history • Custom instructions")

with st.sidebar:
    st.header("Chat settings")
    model = st.selectbox(
        "Model",
        options=list(MODEL_PRICING.keys()),
        index=list(MODEL_PRICING.keys()).index(MODEL_DEFAULT)
        if MODEL_DEFAULT in MODEL_PRICING else 0,
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_output_tokens = st.slider("Maximum output tokens", 128, 2048, 700, 64)
    custom_instructions = st.text_area(
        "Custom instructions",
        value="You are a helpful assistant. Give clear, accurate answers in simple English.",
        height=130,
    )
    json_mode = st.checkbox("Request a JSON response", value=False)
    remember_history = st.checkbox("Include previous chat messages", value=True)

    st.divider()
    st.subheader("Usage")
    st.metric("Input tokens", st.session_state.total_input_tokens)
    st.metric("Output tokens", st.session_state.total_output_tokens)
    cost = estimate_cost(
        model, st.session_state.total_input_tokens, st.session_state.total_output_tokens
    )
    if cost is None:
        st.caption("Cost estimate unavailable for this model.")
    else:
        st.metric("Estimated API cost", f"${cost:.6f}")
    st.caption("Estimates only. Check your provider dashboard for actual billing.")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_input_tokens = 0
        st.session_state.total_output_tokens = 0
        st.rerun()

# Display conversation history.
for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

prompt = st.chat_input("Ask me anything...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status = st.empty()
        status.markdown("Thinking…")
        try:
            client = get_client()
            context = st.session_state.messages if remember_history else [
                {"role": "user", "content": prompt}
            ]

            # Responses API accepts role/content message items. Custom instructions
            # are supplied separately so they do not need to be repeated in history.
            request_args = {
                "model": model,
                "instructions": custom_instructions,
                "input": context,
                "max_output_tokens": max_output_tokens,
                "temperature": temperature,
            }
            if json_mode:
                request_args["text"] = {"format": {"type": "json_object"}}

            response = client.responses.create(**request_args)
            answer = response_text(response)

            usage = getattr(response, "usage", None)
            input_tokens = getattr(usage, "input_tokens", 0) if usage else 0
            output_tokens = getattr(usage, "output_tokens", 0) if usage else 0
            st.session_state.total_input_tokens += input_tokens
            st.session_state.total_output_tokens += output_tokens

            status.empty()
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            with st.expander("Response details"):
                st.write(f"Model: `{model}`")
                st.write(f"Input tokens: `{input_tokens}`")
                st.write(f"Output tokens: `{output_tokens}`")
                estimated = estimate_cost(model, input_tokens, output_tokens)
                if estimated is not None:
                    st.write(f"Estimated cost for this response: `${estimated:.8f}`")

        except RuntimeError as exc:
            status.error(str(exc))
        except RateLimitError:
            status.error("Rate limit or quota reached. Check API usage/billing, then retry.")
        except APIConnectionError:
            status.error("Could not connect to the API. Check your internet connection.")
        except APIStatusError as exc:
            status.error(f"API request failed (HTTP {exc.status_code}). Check the model and API settings.")
        except (ValueError, json.JSONDecodeError):
            status.error("The response could not be processed. Try disabling JSON mode.")
        except Exception as exc:
            status.error(f"Unexpected error: {type(exc).__name__}: {exc}")

st.divider()
st.caption("Security: keep API keys in environment variables. Never commit .env to Git.")
