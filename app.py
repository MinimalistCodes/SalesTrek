import streamlit as st
from langchain_google_genai import GoogleGenerativeAI


from dotenv import load_dotenv
import os, sys

# Load environment variables
load_dotenv()

# Configure Google Gemini API - Remove this section as we will use langchain
api_key = os.getenv("GOOGLE_API_KEY")

# Function to generate the cold call script
def cold_script(industry, keywords, length, tone, scripit_type):
    return f"""
You are a skilled {industry} scriptwriter. Please generate a {scripit_type} script tailored for a sales representative calling potential customers in the {industry} industry. 

The script must be based around the following, and i repeat, MUST BE FORMED AROUND BOTH {industry} & all of the following keywords: {keywords}

**Specific Instructions:**

* **Call Flow:**  
    * **Introduction:** Begin with a warm greeting and introduce yourself and your company.
    * **Value Proposition:** Briefly and compellingly explain the core benefit of your product/service, using the keywords where appropriate.
    * **Qualifying Questions:** Ask open-ended questions to determine if the prospect is a good fit, incorporating the keywords if relevant.
    * **Objection Handling:**  Anticipate and address and list common objections with persuasive rebuttals, potentially referencing the keywords.
    * **Call to Action:** Clearly propose a next step (e.g., schedule a demo, send more information).
    * **Closing:** Thank the prospect for their time and express interest in further discussions.

* **Pain Points:** Research and mention specific pain points relevant to businesses in the {industry} industry, using the keywords to highlight the relevance of your solution.
* **Tone:** Use a {tone} tone that is appropriate for the {industry} industry.
* **Length:** Aim for a script that is approximately {length} in length.
"""


# Function for AI chatbot interaction using langchain
def ai_chatbot(industry, keywords="", length="medium", tone="conversational", scripit_type="cold call"):
    prompt = cold_script(industry, keywords, length, tone, scripit_type)
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)
    st.write(llm.invoke(prompt))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# UI and Chat Logic
st.set_page_config(page_title='Advi Script', layout='wide')
st.title('Advi Script')
st.markdown("An AI-powered tool to generate tailored cold call scripts.")
st.markdown("Provide details about your target industry, preferred tone, script length, and keywords to get a customized script.")
st.markdown("---")
st.markdown("**Example Keywords (comma-separated):** efficiency, cost savings, scalability")

# Display Chat Messages
for message in st.session_state.messages:
    st.markdown(f'**{message["role"]}**: {message["content"]}')

# Form for Input
with st.form("input_form"):
    form_choice = st.selectbox(
        "Select Industry:",
        ["Technology", "Finance", "Healthcare", "Education", "Sales", "Marketing", "Other"]
    )

    if form_choice == "Other":
        other_industry = st.text_input("Please specify the industry:")
        industry = other_industry if other_industry else form_choice
    else:
        industry = form_choice

# Form script type
    form_script_type = st.selectbox("Select Script Type:", ["Cold Call", "Follow-up Call", "Voicemail", "Sales Email", "Other"])

    form_tone = st.selectbox("Select Tone:", ["Professional and Trustworthy", "Casual and conversational", "Persuasive and Assertive", "Empathetic and Supportive", "Energetic and Enthusiastic", "Urgent and persuasive", "Friendly and approachable"])
    form_length = st.selectbox("Select Length:", ["Short", "Medium", "Long"])
    form_keywords = st.text_input("Enter 3 descriptive keywords (comma-separated):")
    

    submitted = st.form_submit_button("Generate Script")
    if submitted:
        keywords_list = [keyword.strip() for keyword in form_keywords.split(",")]
        response = ai_chatbot(industry, form_tone.lower(), form_length.lower(), keywords_list)
        st.session_state.messages.append({"role": "assistant", "content": response})

