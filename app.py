import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
# Your key starting with AIza...
API_KEY = "AIzaSyA6a0Wk_DEvEFhHMEqEOOFvXwwPF6rC6s0"
genai.configure(api_key=API_KEY)

# 2. Page Configuration
st.set_page_config(page_title="Eco-Scan: AI Waste Assistant", page_icon="🌱", layout="centered")
st.title("🌱 Eco-Scan: AI Waste Assistant")
st.markdown("---")

# 3. Model Initialization (Fixing the 404 Error)
# We use the current 2026 stable model names. 
# Gemini 2.5 Flash is the recommended stable upgrade for 1.5 Flash users.
try:
    # Option 1: Try the latest stable 2.5 Flash
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    # Option 2: Fallback to 2.0 Flash (GA version) if 2.5 is unavailable
    model = genai.GenerativeModel('gemini-2.0-flash-001')

# 4. User Interface
uploaded_file = st.file_uploader("Upload a photo of waste items...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Waste Item', use_container_width=True)
    
    # 5. Analysis Logic
    if st.button('Analyze with AI'):
        with st.spinner('Gemini AI is analyzing material...'):
            try:
                # Custom instructions for the AI
                prompt = (
                    "Act as a sustainability expert. Identify the object and its material in this image. "
                    "Provide a report including: 1. Material Type. 2. Is it recyclable? "
                    "3. Step-by-step sustainable disposal instructions."
                )
                
                # Make the API call
                response = model.generate_content([prompt, image])
                
                if response and response.text:
                    st.success("Analysis Complete!")
                    st.markdown("### 📋 AI Disposal Report")
                    st.write(response.text)
                else:
                    st.warning("The AI returned an empty response. Please try a clearer photo.")
                    
            except Exception as e:
                # This will catch and display specific error codes (like 403 or 429)
                st.error(f"Raw API Error: {e}")
                if "403" in str(e):
                    st.info("💡 Your API key is likely blocked. Generate a new key in Google AI Studio.")
                elif "429" in str(e):
                    st.info("💡 You have reached the free tier limit. Wait a few minutes and try again.")
                elif "404" in str(e):
                    st.info("💡 Model not found. The server region may not support this specific model version.")

# 6. Footer
st.markdown("---")
st.caption("Developed by Arka • Powered by Google Gemini 2.5 Flash")
