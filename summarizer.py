import streamlit as st
from langchain.llms import GoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def summarize_text(text):
    llm = GoogleGenerativeAI(temperature=0, google_api_key=api_key) 
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""], chunk_size=1000, chunk_overlap=200
    )
    docs = text_splitter.split_text(text)
    chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run(docs)
    return summary

# UI Layout
st.title("Summarizer")
st.write("Paste the text you want to summarize below:")

# Input Text Area
text_input = st.text_area("Enter text here", height=200)

# Summarize Button
if st.button("Summarize"):
    if text_input:
        with st.spinner("Summarizing..."):
            summary = summarize_text(text_input)
            st.subheader("Summary")
            st.write(summary)
    else:
        st.warning("Please enter some text to summarize.")
