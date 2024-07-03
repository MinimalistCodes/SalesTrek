import streamlit as st
from multipage import MultiPage
from pages import chat_with_coach, sales_script_generator, email_generator, summarizer, image_scan, settings

st.set_page_config(
    page_title="SalesTrek - AI Sales & Marketing Assistant",
    page_icon="🤖",
    layout="wide",
)

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("SalesTrek - AI Sales & Marketing Assistant")


# Add all your applications (pages) here
app.add_page("Chat with Coach", coach_chat.app)
app.add_page("Sales Script Generator", script_gen.app)
app.add_page("Email Generator", email_generator.app)
app.add_page("Summarizer", summarizer.app)
app.add_page("Image Scan", image_scan.app)
app.add_page("Settings", settings.app)

# The main app
app.run()
