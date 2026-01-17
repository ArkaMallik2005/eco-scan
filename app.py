import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Secure API Configuration
# This pulls the key from the 'Secrets' tab in your Streamlit Cloud dashboard.
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
    else:
        st.error("❌ API Key not found in Streamlit Secrets!")
        st.info("Go to: Manage App > Settings > Secrets and add: GOOGLE_API_KEY = 'your_key_here'")
        st.stop()
except Exception as e:
    st.error(f"Error accessing secrets: {e}")
    st.stop()

# 2. Page Configuration
st.set_page_config(page_title="Eco-Scan AI", page_icon="🌱", layout="centered")
st.title("🌱 Eco-Scan: AI Waste Assistant")
st.markdown("---")

# 3. Model Initialization
# We use Gemini 3 Flash as it is the most stable version for 2026.
try:
    model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    st.error(f"Model initialization failed: {e}")
    st.stop()

# 4. User Interface
uploaded_file = st.file_uploader("Upload a photo of waste items...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Captured Waste Item', use_container_width=True)
    
    # 5. Analysis Logic
    if st.button('Analyze with Eco-Scan AI'):
        with st.spinner('Gemini AI is analyzing material...'):
            try:
                # Custom instructions for the AI
                prompt = (
                    "Identify the object and materials. Provide the result in a clean Markdown table with columns: 'Component', 'Material', 'Recycling Symbol', and 'Disposal Action'."
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
                # This will catch specific error codes (like 403 or 429)
                st.error(f"Raw API Error: {e}")
                if "403" in str(e):
                    st.warning("⚠️ This API Key has been blocked or restricted by Google.")

# 6. Footer
st.markdown("---")
st.caption("Developed by Arka • Powered by Google Gemini 2.5 Flash")
