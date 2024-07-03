import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json
from fpdf import FPDF
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from PIL import Image

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def ai_sales_coach(user_input):
    preset_commands = {
        "/help": "Hi there! I'm your AI sales coach. How can I help you?",
        "/features": "I can help with generating scripts, handling objections, sales strategies, and more. Just ask!",
        "/about": "I'm built using Google's Gemini Pro model and LangChain framework.",
        "/clear": "Sure! Let's start fresh. How can I assist you today?", # Clear chat history
        
    }

    # Check for preset commands first
    if user_input in preset_commands:
        return preset_commands[user_input]
    else:
        prompt = f"""
        You are an expert sales coach. You can help with various aspects of sales, including:

        *   Generating cold call scripts
        *   Crafting effective email templates
        *   Providing advice on handling objections
        *   Offering tips for closing deals
        *   Suggesting strategies for prospecting and lead generation
        *   Guiding sales presentations and demos
        *   Sharing best practices for building customer relationships
        *   Explaining sales methodologies and frameworks
        *   Assisting with sales training and coaching
        *   Team building and motivation
        *   Sales management and leadership
        *   Tracking and analyzing sales performance
        *   Sales exercises and role-playing scenarios
        *   Sales forecasting and pipeline management
        *   Sales negotiation tactics and strategies
        *   Recommendations for sales technology and tools
        *   Sales psychology, buyer behavior, and persuasion techniques
        *   Sales ethics and compliance
        *   Emotional intelligence in sales

        Please provide a comprehensive response to the following request:

        {user_input}
    """

        try:
            llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
            return llm.invoke(prompt)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return "Sorry, I couldn't process your request at this time. Please try again later."

# UI Layout
st.title("Advi Script - Your AI Sales Coach")
st.markdown("Ask any sales-related questions or request assistance with specific tasks.")
st.markdown("<small>Chat history is saved in your browser's local storage.</small>", unsafe_allow_html=True)




# Custom CSS for Gemini-like styling with full-screen chat and docked input
st.markdown("""
<style>
body {
    font-family: 'Arial', sans-serif; 
    display: flex; /* Use flexbox for layout */
    flex-direction: column; /* Arrange elements vertically */
    height: 100vh; /* Make the container take up full viewport height */
}
.chat-message {
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
    line-height: 1.5; 
}
.user-message {
    background-color: #F0F0F0; 
    text-align: right;
}
.bot-message {
    background-color: #FFFFFF;
    text-align: left;
}
#chat-input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #FFFFFF;
    padding: 15px;
}
#chat-input { /* Style the textarea for input */
    width: calc(100% - 30px); /* Account for padding */
    resize: vertical; /* Allow vertical resizing */
    min-height: 40px; /* Minimum height */
    max-height: 200px; /* Maximum height */
}
#chat-area {  /* Container for chat messages */
    flex-grow: 1; /* Allow chat area to expand to fill available space */
    overflow-y: auto;  /* Enable scrolling in the chat area */
}
</style>

""", unsafe_allow_html=True)  
sidebar = st.sidebar
sidebar.title("Theme Options")
sidebar.markdown("Customize the appearance of the chat interface.")
#streamlit-extras
# Theme options
theme = sidebar.selectbox("Select a theme", ["Light", "Dark", "Custom"])
if theme == "Light":
    st.markdown(
        """
        <style>
        body {
            background-color: #F0F0F0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
elif theme == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .chat-message {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    custom_css = sidebar.text_area("Custom CSS")
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)
    




# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

    try:
        stored_messages = st.session_state.get("stored_messages", None)
        if stored_messages:
            st.session_state.messages = json.loads(stored_messages)
    except json.JSONDecodeError:
        st.error("Error loading chat history from local storage.")


with st.container():  # Use container for styling
    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
            
   
# User Input
if prompt := st.chat_input("Your message"):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display "Sales Coach is typing..."
    with st.chat_message("assistant"):
        message_placeholder = st.empty() 
        message_placeholder.markdown("Sales Coach is typing...")

    # Get and append AI response (with a delay to simulate typing)
    time.sleep(1)  # Adjust the delay as needed
    response = ai_sales_coach(prompt)
    message_placeholder.markdown(response)  # Update the placeholder
    st.session_state.messages.append({"role": "assistant", "content": response})

col1, col2 = st.columns(2)  # Create two columns for the buttons


st.session_state.stored_messages = json.dumps(st.session_state.messages)