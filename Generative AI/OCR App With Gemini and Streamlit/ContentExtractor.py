import streamlit as st
import os
from PIL import Image

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Function to load OpenAI model and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Document & Image Analyzer")
st.sidebar.title("Upload Image")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.sidebar.file_uploader(
    "Choose an image...", type=["jpg", "png", "jpeg"]
)

# Right portion to show uploaded image
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

submit = st.button("Fetch Information")
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

## If ask button is clicked
if submit:
    if uploaded_file is not None:  # Add this check to ensure file is uploaded
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload an image first.")
