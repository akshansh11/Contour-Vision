# -*- coding: utf-8 -*-
"""contour_app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hukBA3tAzDtJxMhqmazVxJD6rxVPvEDg
"""

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

# Custom CSS for background image
background_image_path = 'eye-4997724.png'
background_css = f"""
<style>
body {{
    background-image: url('data:image/png;base64,{background_image_path}');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}}
</style>
"""

# Function to convert image to base64 for embedding
import base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Embed the background image in the CSS
background_image_base64 = image_to_base64(background_image_path)
background_css = f"""
<style>
body {{
    background-image: url("data:image/png;base64,{background_image_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}}
</style>
"""

# Inject the CSS
st.markdown(background_css, unsafe_allow_html=True)

def process_image(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection
    edges = cv2.Canny(gray_image, 100, 200)

    # Find contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

    return gray_image, edges, contours, contour_image

def plot_images(image, contour_image, edges, gray_image):
    fig, ax = plt.subplots(2, 2, figsize=(15, 10))

    ax[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax[0, 0].set_title("Original Image")
    ax[0, 0].axis('off')

    ax[0, 1].imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))
    ax[0, 1].set_title("Contour Image")
    ax[0, 1].axis('off')

    ax[1, 0].imshow(edges, cmap='gray')
    ax[1, 0].set_title("Edges Detected")
    ax[1, 0].axis('off')

    ax[1, 1].hist(gray_image.ravel(), bins=256, color='black', alpha=0.7)
    ax[1, 1].set_title("Histogram of Grayscale Image")
    ax[1, 1].set_xlabel('Pixel Value')
    ax[1, 1].set_ylabel('Frequency')

    st.pyplot(fig)

def display_contour_info(contours, image):
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        st.write(f"Contour {i+1}: Area = {area:.2f}, Perimeter = {perimeter:.2f}")

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        hull = cv2.convexHull(contour)
        cv2.drawContours(image, [hull], -1, (0, 0, 255), 2)

        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)

    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Contour Image with Annotations", use_column_width=True)

# Streamlit app
st.title("ContourVision")

# Load and display the header image
header_image_path = 'contourvision.png'
st.image(header_image_path, use_column_width=True)

st.write("Upload an image to see contour detection and additional visualizations.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = np.array(Image.open(uploaded_file))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    gray_image, edges, contours, contour_image = process_image(image)

    plot_images(image, contour_image, edges, gray_image)

    st.write(f"Total number of contours found: {len(contours)}")
    display_contour_info(contours, image)