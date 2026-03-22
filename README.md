# AI Resume Analyzer — Setup Guide

## Project Structure
```
resume_analyzer/
├── app.py             ← Streamlit web app (run this)
├── extractor.py       ← Reads TXT / DOCX / Image files
├── cleaner.py         ← Cleans text using NLP
├── train_model.py     ← Trains and saves the ML model
├── analyzer.py        ← ATS score + skill matching + category prediction
├── requirements.txt   ← All libraries needed
└── models/            ← Saved model files go here (created after training)
```

---

## Step 1 — Install libraries
```
pip install -r requirements.txt
```

## Step 2 — Download the dataset
- Go to: https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset
- Download `UpdatedResumeDataSet.csv`
- Place it in this folder (resume_analyzer/)

## Step 3 — Train the model (run ONCE)
```
python train_model.py
```
This creates:  models/model.pkl  |  models/tfidf.pkl  |  models/label_encoder.pkl

## Step 4 — Run the app
```
streamlit run app.py
```
Open http://localhost:8501 in your browser.

---

## For Colab users
- In train_model.py and app.py, Tesseract OCR is optional for Colab
- Comment out the pytesseract path line in extractor.py if running on Colab/Linux
- Install tesseract on Colab with:  !apt-get install tesseract-ocr
