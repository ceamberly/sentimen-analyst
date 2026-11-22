
import pandas as pd


# =====================================
# INDONESIAN SENTIMENT LEXICON
# =====================================

POSITIVE_WORDS = {
    "bagus", "baik", "hebat", "mantap", "keren",
    "sukses", "berhasil", "puas", "senang", "bahagia",
    "setuju", "dukung", "mendukung", "aman", "damai",
    "adil", "bersih", "maju", "terbaik", "positif",
    "terima", "terbantu", "bermanfaat", "stabil",
    "sejahtera", "peduli", "teratasi", "pulih",
    "terjaga", "indah", "cinta", "bangga",
    "makmur", "solusi", "optimis", "mantap"
}

NEGATIVE_WORDS = {
    "buruk", "jelek", "parah", "gagal", "kecewa",
    "marah", "sedih", "benci", "kejam", "rusak",
    "hancur", "bahaya", "ancam", "ancaman", "korupsi",
    "lambat", "mahal", "sulit", "susah", "kacau",
    "kotor", "curang", "bohong", "hoaks", "menipu",
    "rugi", "merugikan", "tolak", "menolak", "protes",
    "krisis", "masalah", "bencana", "parah",
    "kehilangan", "panik", "takut", "cemas",
    "miskin", "gawat", "buruk", "negatif"
}

NEGATION_WORDS = {
    "tidak", "bukan", "belum", "jangan",
    "enggak", "nggak", "gak", "ga", "kurang"
}


# =====================================
# SENTIMENT CLASSIFICATION
# =====================================

def classify_sentiment(text):

    if pd.isna(text):
        text = ""

    words = str(text).lower().split()

    positive_score = 0
    negative_score = 0

    for index, word in enumerate(words):

        # Check negation in the previous 3 words
        previous_words = words[max(0, index - 3):index]

        has_negation = any(
            previous in NEGATION_WORDS
            for previous in previous_words
        )

        if word in POSITIVE_WORDS:

            if has_negation:
                negative_score += 1
            else:
                positive_score += 1

        elif word in NEGATIVE_WORDS:

            if has_negation:
                positive_score += 1
            else:
                negative_score += 1

    score = positive_score - negative_score

    if score > 0:
        label = "Positive"

    elif score < 0:
        label = "Negative"

    else:
        label = "Neutral"

    total_hits = positive_score + negative_score

    if total_hits == 0:
        confidence = "Low"

    elif abs(score) == total_hits:
        confidence = "High"

    else:
        confidence = "Medium"

    return {
        "positive_score": positive_score,
        "negative_score": negative_score,
        "sentiment_score": score,
        "auto_label": label,
        "label": label,
        "confidence": confidence
    }


# =====================================
# DATAFRAME LABELING
# =====================================

def label_dataset(dataframe):

    if dataframe is None or dataframe.empty:
        return pd.DataFrame()

    df = dataframe.copy()

    # Prefer cleaned text for initial classification
    if "cleaned_text" in df.columns:
        text_column = "cleaned_text"

    elif "text" in df.columns:
        text_column = "text"

    else:
        raise ValueError(
            "Dataset must contain 'cleaned_text' or 'text' column."
        )

    results = df[text_column].apply(classify_sentiment)

    df["positive_score"] = results.apply(
        lambda result: result["positive_score"]
    )

    df["negative_score"] = results.apply(
        lambda result: result["negative_score"]
    )

    df["sentiment_score"] = results.apply(
        lambda result: result["sentiment_score"]
    )

    df["auto_label"] = results.apply(
        lambda result: result["auto_label"]
    )

    df["label"] = results.apply(
        lambda result: result["label"]
    )

    df["confidence"] = results.apply(
        lambda result: result["confidence"]
    )

    df["label_source"] = "Automatic"

    return df