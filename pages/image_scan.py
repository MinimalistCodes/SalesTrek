import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import io
from PIL import Image
from st_paywall import Paywall

# Paywall Configuration (replace placeholders with your actual values)
paywall = Paywall(
    stripe_api_key=st.secrets["STRIPE_API_KEY"],
    product_name="Image Scanner Pro",
    product_price_id=st.secrets["STRIPE_PRICE_ID"],
)


def image_scanner():
    st.title("Image Scanner")

    # Check if user is authorized (has paid)
    if paywall.is_authorized():
        # If authorized, display the image scanner functionality
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(bytes_data))
            st.image(image, caption="Uploaded Image.", use_column_width=True)

            if prompt := st.text_input("Ask the AI about the image:"):
                llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
                # image_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
                message = HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {"type": "image", "image": image},
                    ]
                )
                response = llm.invoke([message])
                st.write(response.content)
    else:
        # If not authorized, show the paywall
        paywall.display()


# Run the image scanner
image_scanner()
