import streamlit as st
from streamlit_extras.colored_header import colored_header
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import datetime

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check for API key
if not GOOGLE_API_KEY:
    st.error("Please set your GOOGLE_API_KEY in the .env file.")
    st.stop()

# Configure Google Generative AI
google_genai = GoogleGenerativeAI(api_key=GOOGLE_API_KEY, model_name="models/chat-bison-001")  # Specify model_name

# Prompt Template (dynamically built based on user input)
def cold_script(contents):
    return f"""
You are a skilled sales scriptwriter and coach. A sales rep is looking to craft a cold call script. Based on the information provided so far:

{contents}

Please ask the next logical question to help the sales rep build their script. Keep the question focused on gathering essential information for an effective cold call.
"""

def ai_chatbot(context):
    prompt = cold_script(contents)
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    st.write(llm.invoke(context))


# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hi there! I'm your AI sales coach. Let's craft an awesome cold call script together. First, tell me about the product or service you're selling."})

# UI Design
st.set_page_config(page_title='AdviScript', layout='wide')

colored_header(label="AdviScript", description="AI Sales Coach", color_name="blue-70")
st.markdown("<style>div.stButton > button:first-child {background-color: #007bff; color: white;}</style>", unsafe_allow_html=True)

# Chat Display in Main Area
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.write(f"_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}_")
        st.markdown(message["content"])

# User Input
with st.form(key="user_input", clear_on_submit=True):
    user_input = st.text_input("You:")
    if st.form_submit_button("Send"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Build context for the AI
        context = "\n".join([f"{msg['role']}: {msg['content']}"] for msg in st.session_state.messages)
        
        response = ai_chatbot(context)
        st.session_state.messages.append({"role": "assistant", "content": response})

        st.experimental_rerun()  # Refresh UI to show the new message
