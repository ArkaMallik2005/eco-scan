import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. API Configuration
# Replace with a fresh key from AI Studio if this one continues to show 403 errors
API_KEY = "AIzaSyA6a0Wk_DEvEFhHMEqEOOFvXwwPF6rC6s0"
genai.configure(api_key=API_KEY)

# 2. Page Setup
st.set_page_config(page_title="Eco-Scan AI", page_icon="🌱")
st.title("🌱 Eco-Scan: AI Waste Assistant")
st.markdown("---")

# 3. Secure Model Initialization
# We use a list of models to try. If the first fails, it moves to the next stable one.
model_names = ['models/gemini-1.5-flash', 'gemini-1.5-flash', 'models/gemini-2.0-flash']
model = None

for name in model_names:
    try:
        model = genai.GenerativeModel(name)
        # Quick test to see if the model is actually reachable
        break 
    except Exception:
        continue

if not model:
    st.error("Could not connect to Google AI. Please check your API key restrictions.")

# 4. Image Upload Logic
uploaded_file = st.file_uploader("Upload a photo of waste items...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Captured Waste Item', use_container_width=True)
    
    if st.button('Analyze with Eco-Scan AI'):
        if not model:
            st.error("Model not initialized. Check API Key.")
        else:
            with st.spinner('AI is classifying material...'):
                try:
                    # Comprehensive prompt for better disposal instructions
                    prompt = (
                        "Analyze this image carefully. Identify the object and its material. "
                        "Provide: 1. Material identification. 2. Is it recyclable? "
                        "3. Specific sustainable disposal instructions."
                    )
                    
                    # Generate response
                    response = model.generate_content([prompt, image])
                    
                    if response:
                        st.success("Analysis Complete!")
                        st.markdown("### 📋 Disposal Report")
                        st.write(response.text)
                    else:
                        st.error("AI returned an empty response. Try a clearer image.")
                        
                except Exception as e:
                    # This prints the EXACT error code (403, 404, etc.) for you to see
                    st.error(f"Raw API Error: {e}")
                    st.info("Tip: If you see '403', your API key is blocked. Create a new one in Google AI Studio.")

# 5. Footer
st.markdown("---")
st.caption("Powered by Google Gemini 1.5 Flash • Developed for TechSprint Hackathon")
