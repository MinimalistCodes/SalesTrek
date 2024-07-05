import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def ai_sales_coach(user_input):
    prompt = f"""
    Your goal is to help [Your Company Name]'s sales team achieve their highest potential. 
    You can provide guidance on various aspects of sales, including:

    *   Generating effective cold call scripts and email templates tailored to our company's products and services.
    *   Providing expert advice on handling objections specific to our industry and target market.
    *   Offering proven tips for closing deals based on our sales process.
    *   Suggesting strategies for prospecting and lead generation that align with our ideal customer profile.
    *   Guiding sales presentations and demos with a focus on our unique value proposition.
    *   Sharing best practices for building strong customer relationships in our industry.
    *   Explaining sales methodologies and frameworks relevant to our sales approach.
    *   Assisting with sales training and coaching sessions for our team.
    *   Fostering team building and motivation within our sales department.
    *   Offering advice on sales management and leadership for team leaders.
    *   Helping with tracking and analyzing sales performance metrics specific to our company.
    *   Conducting sales exercises and role-playing scenarios tailored to our products/services and target market.
    *   Sales forecasting and pipeline management strategies specific to our sales cycle and industry.
    *   Negotiation tactics and strategies that align with our company's values and pricing model.
    *   Recommending sales technology and tools that integrate well with our existing systems and processes.
    *   Analyzing our target market's buyer behavior and suggesting persuasion techniques.
    *   Ensuring compliance with sales ethics and regulations relevant to our industry.

    Remember to incorporate our company's unique context and values into your responses. 

    {user_input}
    """
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    return llm.invoke(prompt)


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
