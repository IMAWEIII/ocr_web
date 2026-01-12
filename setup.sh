#!/bin/bash
# Hugging Face Spaces full dependency installer for EasyOCR + Streamlit

echo "=== Starting setup for EasyOCR + Streamlit ==="

# Upgrade pip and build tools
echo "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

# Install CPU-only PyTorch & Torchvision
echo "Installing PyTorch CPU wheels..."
pip install torch==2.1.2 torchvision==0.16.2 -f https://download.pytorch.org/whl/cpu

# Install core dependencies
echo "Installing main Python packages..."
pip install streamlit==1.31.1 \
            numpy==1.24.4 \
            opencv-python-headless==4.8.1.78 \
            easyocr==1.7.1 \
            pillow==10.1.0 \
            mediapipe==0.10.13 \
            matplotlib==3.7.5 \
            googletrans==4.0.0rc1 \
            rich==14.2.0

echo "=== Setup completed successfully! ==="
