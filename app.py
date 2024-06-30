import streamlit as st
import google.generativeai
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check for API key
if not GOOGLE_API_KEY:
    st.error("Please set your GOOGLE_API_KEY in the .env file.")
    st.stop()

# Configure Google Generative AI
google_genai = GoogleGenerativeAI(api_key=GOOGLE_API_KEY)

# Prompt Template (with keywords)
template = """
You are a skilled sales scriptwriter. Please generate a cold call script tailored for a sales representative calling potential customers in the {industry} industry. 

Incorporate these keywords to make the script more relevant: {keywords}

Specific Instructions:

*Call Flow:  
    -Introduction:  Begin with a warm greeting and introduce yourself and your company.
    -Value Proposition:  Briefly and compellingly explain the core benefit of your product/service, using the keywords where appropriate.
    -Qualifying Questions:  Ask open-ended questions to determine if the prospect is a good fit, incorporating the keywords if relevant.
    -Objection Handling:   Anticipate and address common objections with persuasive rebuttals, potentially referencing the keywords.
    -Call to Action:  Clearly propose a next step (e.g., schedule a demo, send more information).

-Pain Points:  Research and mention specific pain points relevant to businesses in the {industry} industry, using the keywords to highlight the relevance of your solution.
-Tone:  Use a {tone} tone that is appropriate for the {industry} industry.
-Length:  Aim for a script that is approximately {length} in length.
"""
prompt_template = PromptTemplate(
    input_variables=["industry", "tone", "length", "keywords"],
    template=template,
)

# AI Chatbot Function
def ai_chatbot(industry, tone="conversational", length="medium", keywords=""):
    prompt = prompt_template.format(industry=industry, tone=tone, length=length, keywords=keywords)
    try:
        response = google_genai(prompt)
    except Exception as e:
        st.error(f"Error generating script: {e}")
        return "Error generating script. Please try again."
    return response

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# UI and Chat Logic
st.set_page_config(page_title='Advi Script', layout='wide')


st.title('Advi Script')
st.markdown("An AI-powered tool to generate tailored cold call scripts.")
st.markdown("Provide details about your target industry, preferred tone, script length, and keywords to get a customized script.")
st.markdown(" Example Keywords (comma-separated):  efficiency, cost savings, scalability")

# Display Chat Messages
for message in st.session_state.messages:
    st.markdown(f' {message["role"]} : {message["content"]}')

# Form for Input
with st.form("input_form"):
    form_choice = st.selectbox(
        "Select Industry:",
        ["Technology", "Finance", "Healthcare", "Education", "Sales", "Other"]
    )

    if form_choice == "Other":
        other_industry = st.text_input("Please specify the industry:")
        industry = other_industry if other_industry else form_choice
    else:
        industry = form_choice

    form_tone = st.selectbox("Select Tone:", ["Conversational", "Professional", "Authoritative"])
    form_length = st.selectbox("Select Length:", ["Short", "Medium", "Long"])
    form_keywords = st.text_input("Enter 3 descriptive keywords (comma-separated):")

# Main function
def main():
    st.title("Cold Call Script Generator")
    st.write("Welcome to the Cold Call Script Generator! Please enter the industry you are targeting and let the AI generate a cold call script for you.")

    industry = st.text_input("Enter the industry you are targeting:")
    if st.button("Generate Cold Call Script"):
        st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": industry})
        ai_chatbot(industry)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write(f"User: {message['content']}")
            else:
                st.write(f"Assistant: {message['content']}")
                
if __name__ == "__main__":
    main()
