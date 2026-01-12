import easyocr
import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

# --- User settings ---
LANGUAGES = ['en']  # Default: English. Example: ['en','es'] for English + Spanish
MAX_WIDTH = 1200    # Maximum width for large images
MAX_HEIGHT = 800    # Maximum height for large images
SAVE_RESULTS = True # Save OCR results as text file

# Initialize EasyOCR reader
reader = easyocr.Reader(LANGUAGES, gpu=False)

def resize_image(img):
    """Resize image if larger than MAX_WIDTH or MAX_HEIGHT while keeping aspect ratio."""
    height, width = img.shape[:2]
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        scaling_factor = min(MAX_WIDTH/width, MAX_HEIGHT/height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
    return img

while True:
    # Open file dialog to select an image
    Tk().withdraw()
    image_path = askopenfilename(title="Select an image")
    
    if not image_path:
        print("No file selected. Exiting.")
        break

    if not os.path.isfile(image_path):
        print("File does not exist. Please try again.")
        continue

    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image. Check file format.")
        continue

    img = resize_image(img)

    # Perform OCR
    results = reader.readtext(img)

    if not results:
        print("No text detected in this image.")
    else:
        full_text = ""
        # Draw OCR results
        for bbox, text, confidence in results:
            full_text += f"{text} (Confidence: {confidence:.2f})\n"
            pts = [(int(x), int(y)) for x, y in bbox]
            cv2.polylines(img, [np.array(pts)], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(img, text, (pts[0][0], pts[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Save OCR results to text file
        if SAVE_RESULTS:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            text_file_path = os.path.join(os.path.dirname(image_path), f"{base_name}_ocr.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"OCR results saved to: {text_file_path}")

        # Show image with OCR results
        cv2.imshow("OCR Result", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
