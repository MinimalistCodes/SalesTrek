import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json
from fpdf import FPDF
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from PIL import Image
import runtimes as rt

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

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

    try:
        stored_messages = st.session_state.get("stored_messages", None)
        if stored_messages:
            st.session_state.messages = json.loads(stored_messages)
    except json.JSONDecodeError:
        st.error("Error loading chat history from local storage.")


# Main Chat Area
with st.container():
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Box at the Bottom (Docked and Centered)
    with st.container():  # Create a container for centering
        with st.form(key="chat_form"):
            user_input = st.text_area("Your message", key="chat_input", height=40, max_chars=None)
            submitted = st.form_submit_button("Send")
            if submitted:
                if user_input:  
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    with st.chat_message("user"):
                        st.markdown(user_input)

                    # Display "Sales Coach is typing..." message
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty() 
                        message_placeholder.markdown("Sales Coach is typing...")

                    # Get AI response with a slight delay to simulate typing
                    time.sleep(1)  # Adjust delay as needed
                    response = ai_sales_coach(user_input)
                    st.session_state.messages.append({"role": "assistant", "content": response})

                    # Update the placeholder with the actual response
                    message_placeholder.markdown(response) 

                    # Clear the input box after sending the message
                    st.session_state.chat_input = ""

                    # Save chat history to local storage
                    st.session_state.stored_messages = json.dumps(st.session_state.messages)


# Buttons in a Row (under the input box)
with st.container():
    st.markdown("<div id='button-container'>", unsafe_allow_html=True)  # Button container
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear History"):
            # Clear chat history (same as before)
            st.session_state.messages = []
            st.session_state.pop("stored_messages", None)
            st.experimental_rerun()

    with col2:
        if st.button("Export Chat to PDF"):
            # Export to PDF (same as before)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for message in st.session_state.messages:
                role = message["role"].capitalize()
                content = message["content"]
                pdf.cell(200, 10, txt=f"{role}: {content}", ln=True, align="L")

            pdf_output = pdf.output(dest="S").encode("latin-1")
            st.download_button(
                label="Download PDF",
                data=pdf_output,
                file_name="chat_history.pdf",
                mime="application/pdf",
            )
    st.markdown("</div>", unsafe_allow_html=True)  # Close button container