import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import os

# Function to sharpen the image
def sharpen_image(image, strength):
    kernel = np.array([[0, -strength, 0],
                       [-strength, 1 + 4 * strength, -strength],
                       [0, -strength, 0]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened

# Function to smooth the image
def smooth_image(image, strength):
    ksize = int(2 * round(strength) + 1)  # Kernel size must be odd
    smoothed = cv2.GaussianBlur(image, (ksize, ksize), 0)
    return smoothed

# Streamlit App
st.title("Image Sharpening and Smoothing Tool")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Read the uploaded image
    original_name = os.path.splitext(uploaded_file.name)[0]  # Extract file name without extension
    image = Image.open(uploaded_file)
    image_array = np.array(image)

    # Display the original image
    st.subheader("Original Image")
    st.image(image_array, channels="RGB")

    # Choose between sharpening or smoothing
    choice = st.radio("Choose an option:", ["Sharpen", "Smooth"])

    # Slider for strength adjustment
    if choice == "Sharpen":
        strength = st.slider("Sharpening Strength", min_value=0.0, max_value=2.0, value=0.5, step=0.1)
        processed_image = sharpen_image(image_array, strength)
        suffix = "_sharpened"
    else:
        strength = st.slider("Smoothing Strength", min_value=1.0, max_value=10.0, value=3.0, step=1.0)
        processed_image = smooth_image(image_array, strength)
        suffix = "_smoothed"

    # Display the processed image
    st.subheader("Processed Image")
    st.image(processed_image, channels="RGB")

    # Convert the processed image to PIL format for downloading
    processed_pil_image = Image.fromarray(processed_image)
    if processed_pil_image.mode != "RGB":
        processed_pil_image = processed_pil_image.convert("RGB")

    # Prepare the image for download
    buffer = io.BytesIO()
    processed_pil_image.save(buffer, format="JPEG")
    buffer.seek(0)

    # Set the download filename
    download_filename = f"{original_name}{suffix}.jpg"

    # Download button
    st.download_button(
        label="Download Processed Image",
        data=buffer,
        file_name=download_filename,
        mime="image/jpeg"
    )
