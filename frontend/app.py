import sys
from pathlib import Path

import streamlit as st

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.app import generate_response


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Production AI Application",
    page_icon="🤖",
    layout="centered",
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🤖 Production AI Application")

st.write(
    "A production-style AI application built step by step "
    "with Google Gemini."
)


# ---------------------------------------------------------
# Conversation History
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# ---------------------------------------------------------
# Chat Input
# ---------------------------------------------------------

user_input = st.chat_input("Ask the AI something...")


if user_input:

    # Store user message immediately
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    # -----------------------------------------------------
    # Generate AI response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            try:
                result = generate_response(user_input)

                response = result.response

                st.write(response)

                # Store assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

            except Exception as error:
                st.error(f"Something went wrong: {error}")