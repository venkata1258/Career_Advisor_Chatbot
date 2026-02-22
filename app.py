import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from chatbot.env
load_dotenv("chatbot.env")

# Get Gemini API key from environment
gemini_key = os.getenv("gemini_project")

if not gemini_key:
    st.error("Gemini API key not found. Set it in chatbot.env.")
    st.stop()

# Set API key for Gemini client
os.environ["GOOGLE_API_KEY"] = gemini_key

# Initialize Gemini client
client = genai.Client()

# System prompt for career advisor
SYSTEM_PROMPT = """
You are an expert AI Career Advisor.

Your responsibilities:
- Provide structured career guidance
- Suggest skills, certifications, tools
- Provide roadmap in bullet format
- Be concise and professional
- Do NOT provide medical or legal advice
- If question is outside career domain, politely redirect

Response Format:
1. Overview
2. Required Skills
3. Recommended Learning Path
4. Career Opportunities
"""

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.set_page_config(page_title="Career Advisor Chatbot", page_icon="🤖")
st.title("AI Career Advisor Chatbot 🤖")
st.write("Ask career-related questions and get structured guidance.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_query = st.chat_input("Ask a career-related question...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"{SYSTEM_PROMPT}\n\nUser: {user_query}"
        )
        answer = response.text
    except Exception:
        answer = "⚠️ Error generating response. Please try again."

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)

# Clear chat
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()