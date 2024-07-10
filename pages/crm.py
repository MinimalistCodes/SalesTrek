import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json
from fpdf import FPDF


# Load environment va   riables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def ai_sales_coach(user_input):
      llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
      return llm.invoke(user_input)


st.set_page_config(
    page_title="SalesTrek - Customer Management System",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)


#load styles.css
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


with st.sidebar:
    # clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
    st.markdown("---")  # Horizontal line
    #save to pdf button
    if st.button("Save Chat to PDF"):
        #use FPDF to save chat to pdf
        pdf_file = save_chat_to_pdf(st.session_state.messages)
        st.success(f"Chat history saved to {pdf_file}")
    st.markdown("---")  # Horizontal line
    # Chatbot settings
    st.markdown("### Chatbot Settings")
    st.markdown("Customize the chatbot settings.")
    # Chatbot settings form
    chatbot_settings = st.form("chatbot_settings")
    with chatbot_settings:
        # Chatbot settings form fields
        st.markdown("#### Chatbot Settings")
        st.info("Enter your Google API Key to enable the AI Sales Coach. (Get your API Key from the Google Cloud Console.)")
        # Chatbot settings form fields
        api_key = st.text_input("API Key", value=api_key)
        #if blank set to default
        if not api_key:
            api_key = os.getenv("GOOGLE_API_KEY")
        # Save button
        submit_button = st.form_submit_button("Save")
    # Save chatbot settings
    if submit_button:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.success("Chatbot settings saved successfully.")
#----------------------------------
#Simple CRM
crm = {}
#----------------------------------
# Full Page CRM

st.title("Customer Relationship Management")
st.markdown("Manage your customer relationships.")

# CRM form
crm_form = st.form("crm_form")
with crm_form:
    st.markdown("### Add Customer")
    customer_name = st.text_input("Name")
    customer_email = st.text_input("Email")
    customer_phone = st.text_input("Phone")
    submit_button = st.form_submit_button("Add")
    
# Save customer
if submit_button:
    crm[customer_email] = {"name": customer_name, "phone": customer_phone}
    st.success(f"Customer {customer_name} added successfully.")
    
# Display customers
if crm:
    st.markdown("### Customers")
    for email, customer in crm.items():
        st.markdown(f"**{customer['name']}**")
        st.markdown(f"Email: {email}")
        st.markdown(f"Phone: {customer['phone']}")
        
#----------------------------------



  
