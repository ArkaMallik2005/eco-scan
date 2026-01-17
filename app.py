import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API Key
API_KEY = "AIzaSyBuPobmkf9EmEoThUfnydPwJklgyCbnGh4"
genai.configure(api_key=API_KEY)

# 2. Page Configuration
st.set_page_config(page_title="Eco-Scan", page_icon="🌱")
st.title("🌱 Eco-Scan: AI Waste Assistant")

# 3. Model Initialization with Error Handling
# We use the explicit model string to avoid the "NotFound" error
try:
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"Model initialization failed: {e}")

# 4. User Interface
uploaded_file = st.file_uploader("Choose an image of waste...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    if st.button('Analyze Waste'):
        with st.spinner('Analyzing with Gemini AI...'):
            try:
                # Prompt for the AI
                prompt = (
                    "Identify the object in this image. Provide a clear report on: "
                    "1. Material Type. 2. Recyclability status. 3. Best sustainable disposal method."
                )
                
                # Generating content
                response = model.generate_content([prompt, image])
                
                # Display results
                st.success("Analysis Complete!")
                st.markdown("### AI Analysis Results")
                st.write(response.text)
                
            except Exception as e:
                # This will show the EXACT error message if it fails again
                st.error("The AI service is currently unavailable or the API key has reached its limit.")
                st.info(f"Technical details for debugging: {e}")
