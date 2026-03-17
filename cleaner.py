# ============================================================
# cleaner.py - ADVANCED VERSION
# Better NLP preprocessing using tokenization
# ============================================================

import re
import string
import nltk

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPWORDS = set(stopwords.words('english'))
PUNCT = str.maketrans({p: " " for p in string.punctuation})

def clean_text(text):
    """
    Advanced text cleaning pipeline:
    1. Lowercase
    2. Remove URLs, emails, phone numbers
    3. Remove punctuation
    4. Tokenize (split into words properly)
    5. Remove stopwords and short words
    6. Rejoin into clean string
    """
    if not isinstance(text, str):
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # 3. Remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # 4. Remove phone numbers
    text = re.sub(r'\+?\d[\d\s\-().]{7,}', ' ', text)

    # 5. Replace punctuation with spaces
    text = text.translate(PUNCT)

    # 6. Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # 7. Tokenize
    try:
        tokens = word_tokenize(text)
    except:
        tokens = text.split()

    # 8. Keep only alphabetic tokens, remove stopwords, remove short words
    tokens = [
        t for t in tokens
        if t.isalpha()
        and t not in STOPWORDS
        and len(t) > 2
    ]

    return ' '.join(tokens)


if __name__ == "__main__":
    sample = "Hi! I'm a Python Developer at Google. Visit http://google.com | Email: dev@google.com"
    print("Before:", sample)
    print("After: ", clean_text(sample))
