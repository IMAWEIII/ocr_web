---
title: EasyOCR + Translation Web App
emoji: 🌐
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.31.1
app_file: app.py
python_version: 3.13
pinned: false
---


# EasyOCR + Translation Web App

This app detects text using EasyOCR and can translate it. Built with Streamlit.

## How to run

1. Click **Deploy** on Hugging Face Spaces.
2. Or run locally:

```bash
# optional: create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# install dependencies
pip install -r requirements.txt

# run the app
streamlit run app.py
