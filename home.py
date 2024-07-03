from datetime import datetime
import time

import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json
from fpdf import FPDF
from streamlit_extras.switch_page_button import switch_page
from PIL import Image


# Home Page Content
def app():
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
    st.markdown("<h1 style='text-align: center;'>🚀 Welcome to SalesTrek</h1>", unsafe_allow_html=True)
    # You can add your about section content here
    st.write("""
    With features like AI Sales Coach, Sales Script Generator, Email Generator, and more, SalesTrek provides valuable insights and resources to enhance your sales strategies and boost your performance. Explore our range of tools and take your sales game to the next level with SalesTrek!
    """)
    st.markdown("---")
    st.markdown("### ✨Features")
        #markdown table
    st.markdown("""
        | Feature | Description |
        | --- | --- |
        | AI Sales Coach | Get expert advice and guidance on sales strategies, objection handling, and more. |
        | Sales Script Generator | Generate custom sales scripts and email templates tailored to your needs. |
        | Email Generator | Create engaging and effective email templates for your sales campaigns. |
        | Summarizer | Summarize long texts or articles quickly and efficiently. |
        | Image Scan | Analyze images and extract text for further processing. |
        | Settings | Customize your SalesTrek experience with personalized settings. |
        """)
    st.markdown("---")
    st.markdown("### 🤔 How to Use")
        #Step by step instructions
    st.markdown("""
        1. **Select a Feature**: Choose a feature from the sidebar menu.
        2. **Input Data**: Enter the required data or content for the selected feature.
        3. **Click on the Button**: Click on the corresponding button to run the feature.
        4. **View Results**: Review the results or output generated by the feature.
        """)
    st.markdown("---")
    st.markdown("### 📅 Upcoming Features")
    st.markdown("""
                    - **Sales Forecasting**: Predict future sales trends and outcomes based on historical data.
                    - **Lead Scoring**: Identify and prioritize high-quality leads for better conversion rates.
                    - **CRM Integration**: Connect SalesTrek with your CRM system for seamless data management.
                    - **Sales Analytics**: Analyze sales performance and metrics to optimize your strategies.
                    - **Voice Assistant**: Interact with SalesTrek using voice commands for hands-free operation.
                    """)
                    
app()