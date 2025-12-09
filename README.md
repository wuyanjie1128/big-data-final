# Global Animal Explorer 🐾

An all-English Streamlit app designed for GitHub + Streamlit Cloud.

## Core Goals
- **No Chinese text in the UI**
- **Animal Name Explorer** shows image + popular-science info
- **Image Animal Identifier** works **without any API key**
- **Global coverage** via GBIF (millions of species)

## Features

### ⭐ Featured Categories
Curated representative animals across major groups.

### 🔎 Animal Name Explorer (No API key)
Type a name:
- Finds a Featured match (common name / scientific name / aliases)
- If no local match, validates via GBIF.

### 🌍 Global Animal Encyclopedia (GBIF)
Search the GBIF backbone taxonomy.

### 🧠 Image Animal Identifier (No API key)
Uses a lightweight onboard ImageNet classifier via ONNX.
Best for general identification and animal group-level recognition.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
