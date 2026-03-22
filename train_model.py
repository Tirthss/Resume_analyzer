# ============================================================
# train_model.py - ADVANCED VERSION
# Uses SVM + TF-IDF with better preprocessing
# Prints accuracy, precision, recall, F1 score
# ============================================================

import pandas as pd
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, precision_score,
                             recall_score, f1_score)
from cleaner import clean_text

print("="*60)
print("   AI RESUME ANALYZER - MODEL TRAINING")
print("="*60)

# ── 1. LOAD DATASET ──────────────────────────────────────────
print("\n[1/6] Loading dataset...")

dataset_path = 'UpdatedResumeDataSet.csv'
if not os.path.exists(dataset_path):
    print(f"ERROR: '{dataset_path}' not found!")
    exit()

df = pd.read_csv(dataset_path)

# Handle both column name formats
if 'Resume_str' in df.columns:
    df = df.rename(columns={'Resume_str': 'Resume'})
elif 'Resume' not in df.columns:
    # Try to find the resume text column
    text_cols = [c for c in df.columns if c.lower() not in ['category', 'id']]
    if text_cols:
        df = df.rename(columns={text_cols[0]: 'Resume'})

# Drop nulls and duplicates
df = df.dropna(subset=['Resume', 'Category'])
df = df.drop_duplicates(subset=['Resume'])
df = df[df['Resume'].str.len() > 50]  # remove very short entries

print(f"    Loaded: {len(df)} resumes")
print(f"    Categories: {df['Category'].nunique()}")
print(f"    Category list:")
for cat, count in df['Category'].value_counts().items():
    print(f"      {cat:40} : {count}")

# ── 2. CLEAN TEXT ────────────────────────────────────────────
print("\n[2/6] Cleaning and preprocessing text...")
df['cleaned'] = df['Resume'].apply(clean_text)

# Remove empty cleaned texts
df = df[df['cleaned'].str.len() > 10]
print(f"    Done! {len(df)} resumes after cleaning.")

# ── 3. ENCODE LABELS ─────────────────────────────────────────
print("\n[3/6] Encoding category labels...")
le = LabelEncoder()
df['label'] = le.fit_transform(df['Category'])
print(f"    {df['Category'].nunique()} unique categories encoded.")

# ── 4. TF-IDF VECTORIZATION ──────────────────────────────────
print("\n[4/6] Running TF-IDF vectorization...")

# ngram_range=(1,2) means single words AND two-word phrases
# This captures "machine learning", "data science" etc. as single features
tfidf = TfidfVectorizer(
    max_features=10000,       # top 10k most important words
    ngram_range=(1, 2),       # unigrams + bigrams
    sublinear_tf=True,        # better scaling for long docs
    min_df=2,                 # word must appear in at least 2 docs
    stop_words='english'
)

X = tfidf.fit_transform(df['cleaned'])
y = df['label']

print(f"    Feature matrix: {X.shape[0]} resumes × {X.shape[1]} features")

# ── 5. TRAIN / TEST SPLIT ────────────────────────────────────
print("\n[5/6] Splitting data and training model...")

# stratify=y ensures each category is proportionally represented
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"    Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")

# ── LinearSVC is much faster than SVC and equally accurate ───
# CalibratedClassifierCV wraps it to give probability scores
print("    Training LinearSVC (fast + accurate for text)...")
base_model = LinearSVC(max_iter=2000, C=1.0)
model = CalibratedClassifierCV(base_model, cv=3)
model.fit(X_train, y_train)
print("    Training complete!")

# ── 6. EVALUATE ──────────────────────────────────────────────
print("\n[6/6] Evaluating model performance...")

y_pred = model.predict(X_test)

accuracy  = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall    = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1        = f1_score(y_test, y_pred, average='weighted', zero_division=0)

print("\n" + "="*60)
print("   MODEL PERFORMANCE REPORT")
print("="*60)
print(f"   Accuracy  : {accuracy*100:.2f}%")
print(f"   Precision : {precision*100:.2f}%")
print(f"   Recall    : {recall*100:.2f}%")
print(f"   F1 Score  : {f1*100:.2f}%")
print("="*60)

# Cross validation score (more reliable than single split)
print("\n   Running 5-fold cross validation...")
cv_scores = cross_val_score(
    CalibratedClassifierCV(LinearSVC(max_iter=2000, C=1.0), cv=3),
    X, y, cv=5, scoring='accuracy'
)
print(f"   CV Accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")

# Detailed per-category report
print("\n   Per-Category Report:")
print(classification_report(
    y_test, y_pred,
    target_names=le.classes_,
    zero_division=0
))

# ── SAVE ─────────────────────────────────────────────────────
os.makedirs('models', exist_ok=True)
pickle.dump(model, open('models/model.pkl', 'wb'))
pickle.dump(tfidf, open('models/tfidf.pkl',  'wb'))
pickle.dump(le,    open('models/label_encoder.pkl', 'wb'))

print("="*60)
print("   Model saved to models/")
print("   models/model.pkl")
print("   models/tfidf.pkl")
print("   models/label_encoder.pkl")
print("="*60)
print("\n   Now run: streamlit run app.py")
