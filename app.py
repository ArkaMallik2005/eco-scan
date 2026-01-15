import os
import subprocess
import sys

# Force installation of missing modules
try:
    import google.generativeai as genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

import streamlit as st
from PIL import Image

genai.configure(api_key="AIzaSyA6a0Wk_DEvEFhHMEqEOOFvXwwPF6rC6s0")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.title("🌱 Eco-Scan: AI Waste Assistant")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    if st.button('Analyze Waste'):
        with st.spinner('Analyzing...'):
            prompt = "Identify the object in this image. Tell me: 1. What material it is. 2. If it is recyclable. 3. The best way to dispose of it sustainably."
            response = model.generate_content([prompt, image])
            st.success("Analysis Complete!")
            st.write(response.text)
