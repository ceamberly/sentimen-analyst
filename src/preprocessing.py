
import re
import pandas as pd

from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory
)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


# =====================================
# INITIALIZATION
# =====================================

stopword_factory = StopWordRemoverFactory()
stopwords = set(stopword_factory.get_stop_words())

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

# Kata negasi penting untuk analisis sentimen.
# Jangan sampai kata-kata ini ikut dihapus.
important_words = {
    "tidak", "bukan", "belum", "jangan",
    "kurang", "tanpa", "enggak", "nggak",
    "gak", "ga"
}

stopwords = stopwords - important_words


# =====================================
# TEXT CLEANING
# =====================================

def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    # Hapus URL
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Hapus mention dan hashtag
    text = re.sub(r"@\w+|#\w+", " ", text)

    # Hapus angka
    text = re.sub(r"\d+", " ", text)

    # Hapus karakter selain huruf
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Hapus spasi berlebih
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =====================================
# TOKENIZATION
# =====================================

def tokenize_text(text):
    if not text:
        return []

    return text.split()


# =====================================
# STOPWORD REMOVAL
# =====================================

def remove_stopwords(tokens):
    return [
        word for word in tokens
        if word not in stopwords
    ]


# =====================================
# STEMMING
# =====================================

def stemming_text(tokens):
    text = " ".join(tokens)

    if not text:
        return ""

    return stemmer.stem(text)


# =====================================
# COMPLETE PREPROCESSING
# =====================================

def preprocess_text(text):
    cleaned = clean_text(text)

    tokens = tokenize_text(cleaned)

    filtered_tokens = remove_stopwords(tokens)

    stemmed = stemming_text(filtered_tokens)

    return {
        "cleaned_text": cleaned,
        "tokens": tokens,
        "filtered_tokens": filtered_tokens,
        "stemmed_text": stemmed
    }


# =====================================
# PREPROCESS DATASET
# =====================================

def preprocess_comments(dataframe):
    if dataframe is None or dataframe.empty:
        return pd.DataFrame()

    if "text" not in dataframe.columns:
        raise ValueError(
            "Dataset tidak memiliki kolom 'text'."
        )

    df = dataframe.copy()

    # Hapus komentar kosong
    df["text"] = df["text"].fillna("").astype(str)
    df = df[df["text"].str.strip() != ""].copy()

    # Hapus komentar duplikat
    df = df.drop_duplicates(subset=["text"]).copy()

    # Proses teks
    results = df["text"].apply(preprocess_text)

    df["cleaned_text"] = results.apply(
        lambda x: x["cleaned_text"]
    )

    df["tokens"] = results.apply(
        lambda x: x["tokens"]
    )

    df["filtered_tokens"] = results.apply(
        lambda x: x["filtered_tokens"]
    )

    df["stemmed_text"] = results.apply(
        lambda x: x["stemmed_text"]
    )

    # Hapus hasil preprocessing yang kosong
    df = df[df["stemmed_text"].str.strip() != ""].copy()

    return df.reset_index(drop=True)