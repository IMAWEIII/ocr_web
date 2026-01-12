import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator

# --- App Title ---
st.set_page_config(page_title="EasyOCR + Translator", layout="wide")
st.title("🌐 EasyOCR + Translation Web App")
st.write("Upload an image, detect text in any language, and translate it instantly!")

# --- OCR language selection ---
langs = st.multiselect(
    "Select OCR language(s) for detection:",
    options=["en", "es", "fr", "de", "pt", "it", "zh", "ja", "ko", "ar", "hi", "ru"],
    default=["en"]
)

# --- Target language for translation ---
target_lang = st.selectbox(
    "Translate detected text to:",
    options=["en", "es", "fr", "de", "pt", "it", "zh-cn", "ja", "ko", "ar", "hi", "ru"],
    index=0
)

# --- Upload image ---
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file:
    # Open image
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    # Resize large images
    max_dim = 1024
    h, w = img_np.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img_np = cv2.resize(img_np, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
        st.write(f"Image resized to {img_np.shape[1]}x{img_np.shape[0]}")

    st.image(img_np, caption="Uploaded Image", use_column_width=True)

    # --- Initialize EasyOCR ---
    with st.spinner("Loading OCR model..."):
        reader = easyocr.Reader(langs, gpu=False)

    # --- Fix for PIL.ANTIALIAS in EasyOCR ---
    import PIL
    if not hasattr(PIL.Image, "ANTIALIAS"):
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

    # --- Perform OCR ---
    with st.spinner("Scanning text..."):
        results = reader.readtext(img_np)

    if not results:
        st.warning("No text detected!")
    else:
        # Convert to PIL for proper Unicode support
        img_pil = Image.fromarray(img_np)
        draw = ImageDraw.Draw(img_pil)

        # Load a font that supports multiple languages
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        # Initialize translator
        translator = Translator()

        # Draw bounding boxes + translated text
        for bbox, text, confidence in results:
            pts = [(int(x), int(y)) for x, y in bbox]
            draw.line(pts + [pts[0]], fill=(0, 255, 0), width=2)

            # Translate text
            try:
                translated = translator.translate(text, dest=target_lang).text
            except:
                translated = text

            # Draw original + translated text above the box
            draw.text((pts[0][0], pts[0][1]-35), f"{text} → {translated}", fill=(255, 0, 0), font=font)

        # Show result
        st.image(np.array(img_pil), caption="OCR + Translation Result", use_column_width=True)

        # --- Display Detected + Translated Text ---
        st.subheader("Detected & Translated Text:")
        for bbox, text, confidence in results:
            try:
                translated = translator.translate(text, dest=target_lang).text
            except:
                translated = text
            st.write(f"**Original:** {text}  →  **Translated:** {translated} (Confidence: {confidence:.2f})")
