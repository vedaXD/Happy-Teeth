import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure API key for Google Generative AI
genai.configure(api_key=os.environ["AI_KEY"])

def analyze_image(image):
    # Placeholder for image analysis logic
    # You would pass the image to an AI model here for processing
    # Example: Return a dummy analysis result
    return "Analysis result: This is a placeholder result for the image analysis."

# Set up the Streamlit interface
st.title("Happy Teeth AI Assistant 🦷")
st.write("Hey there! I'm Happy Teeth🦷. How should I help you?")
st.write("Upload an image of your teeth for analysis by Happy Teeth.")

uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Analyze the image directly
    result = analyze_image(image)
    st.write(result)

    # Chat session setup
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="""
        You are an AI dental assistant, Happy Teeth.
        When a user uploads an image, treat it as a dental image that needs analysis. 
        Analyze the image content directly and suggest potential dental issues based on what you observe.
        """,
    )

    st.write("Analyzing the image...")

    # Pass an image-related prompt to the model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Here is an image of my teeth, please analyze it for any dental issues."
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Thank you! I'll analyze the image now."
                ],
            }
        ]
    )

    # Send a message to the model for analysis
    response = chat_session.send_message("Please analyze the provided image for any dental issues.")

    st.write(response.text)
