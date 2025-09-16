import streamlit as st

from PIL import Image
from backend.generate_img import generate_image
from backend.diffusion_pipeline import pipe

st.title("Prompt + Image Guided Diffusion Generator")

uploaded_file = st.file_uploader("Choose an image", type=["png","jpg","jpeg"])
prompt = st.text_input("Enter your prompt")

if st.button("Generate"):
    if uploaded_file and prompt:
        input_img = Image.open(uploaded_file)
        output_img = generate_image(prompt, input_img, pipe)
        st.image(output_img, caption="Generated Image")
    else:
        st.warning("Please upload an image and enter a prompt.")
