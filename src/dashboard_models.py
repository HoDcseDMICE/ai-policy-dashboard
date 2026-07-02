"""
Lightweight NLP/ML helpers for the AI Policy Dashboard.
Provides:
- LDA topic modeling (sklearn)
- Optional BERTopic wrapper (if installed)
- Sentiment scoring -> labels: Enabling / Restrictive / Neutral
- Document clustering (TF-IDF + KMeans)
- Optional impact prediction (Ridge regression)

These functions are written to work with small/medium CSVs in `data/` and
are defensive about missing optional dependencies.
"""
from typing import List, Dict, Any, Tuple, Optional
import re
import numpy as np
import pandas as pd

# Core ML/NLP imports
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

# Try optional libraries
try:
    from textblob import TextBlob
except Exception:
    TextBlob = None

try:
    from bertopic import BERTopic
except Exception:
    BERTopic = None


def _clean_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return s.strip()


def lda_topics(texts: List[str], n_topics: int = 10, n_top_words: int = 10) -> Dict[str, Any]:
    """Run LDA and return topics and doc-topic matrix.

    Returns:
      {
        "topics": [{"topic_id": int, "words": [str,...], "weights": [float,...]}],
        "doc_topic_matrix": ndarray (n_docs x n_topics)
      }
    """
    cleaned = [_clean_text(t) for t in texts]
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")
    dtm = vectorizer.fit_transform(cleaned)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    doc_topic = lda.fit_transform(dtm)

    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[::-1][:n_top_words]
        topics.append({
            "topic_id": int(topic_idx),
            "words": [feature_names[i] for i in top_indices],
            "weights": [float(topic[i]) for i in top_indices]
        })
    return {"topics": topics, "doc_topic_matrix": doc_topic}


def bertopic_topics(texts: List[str], min_topic_size: int = 10) -> Dict[str, Any]:
    """Run BERTopic if installed. Returns topics and assignments.

    Raises a helpful error if BERTopic is not installed.
    """
    if BERTopic is None:
        raise RuntimeError("BERTopic is not installed. Install with `pip install bertopic` to use this function.")
    try:
        model = BERTopic(min_topic_size=min_topic_size)
        topics, probs = model.fit_transform(texts)
        topic_info = model.get_topic_info()
        return {"model": model, "topics": topic_info.to_dict(orient="records"), "assignments": topics, "probs": probs}
    except Exception as e:
        # Provide an informative error without crashing the app
        raise RuntimeError(f"BERTopic failed to run: {e}")


def sentiment_label(texts: List[str], threshold: float = 0.1) -> pd.DataFrame:
    """Compute a sentiment polarity and map to labels.

    Mapping (default): polarity > threshold -> Enabling
                     polarity < -threshold -> Restrictive
                     else -> Neutral

    Uses TextBlob if available; otherwise falls back to a naive keyword heuristic.
    Returns DataFrame with columns: `text`, `polarity`, `label`
    """
    records = []
    for t in texts:
        if TextBlob is not None:
            try:
                polarity = TextBlob(t).sentiment.polarity
            except Exception:
                polarity = 0.0
        else:
            # fallback heuristic: count positive/negative words
            txt = _clean_text(t)
            pos_words = ["support", "enable", "promote", "encourage", "allow"]
            neg_words = ["restrict", "ban", "prohibit", "limit", "discourage"]
            p = sum(txt.count(w) for w in pos_words)
            n = sum(txt.count(w) for w in neg_words)
            polarity = (p - n) / (max(1, p + n)) if (p + n) > 0 else 0.0
        if polarity > threshold:
            label = "Enabling"
        elif polarity < -threshold:
            label = "Restrictive"
        else:
            label = "Neutral"
        records.append({"text": t, "polarity": float(polarity), "label": label})
    return pd.DataFrame.from_records(records)


def cluster_documents(texts: List[str], n_clusters: int = 5, top_n_terms: int = 10) -> Dict[str, Any]:
    """Cluster documents using TF-IDF + KMeans and return labels and top terms per cluster."""
    cleaned = [ _clean_text(t) for t in texts ]
    tf = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    X = tf.fit_transform(cleaned)
    if X.shape[0] == 0:
        return {"labels": [], "top_terms": []}
    kmeans = KMeans(n_clusters=min(n_clusters, X.shape[0]), random_state=42)
    labels = kmeans.fit_predict(X)
    terms = tf.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    top_terms = []
    for i in range(kmeans.n_clusters):
        top = [terms[ind] for ind in order_centroids[i, :top_n_terms]]
        top_terms.append({"cluster": int(i), "terms": top})
    return {"labels": labels.tolist(), "top_terms": top_terms}


def impact_predict(features: pd.DataFrame, target: str, test_size: float = 0.2, random_state: int = 42) -> Dict[str, Any]:
    """Fit a simple Ridge regression to predict `target` from `features`.

    Returns dict with model, metrics and optional predictions on test set.
    Raises ValueError if target not in features.
    """
    if target not in features.columns:
        raise ValueError(f"Target column '{target}' not found in dataframe")
    X = features.drop(columns=[target])
    y = features[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    model = Ridge()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    metrics = {"r2": float(r2_score(y_test, preds)), "mse": float(mean_squared_error(y_test, preds))}
    return {"model": model, "metrics": metrics, "y_test": y_test.tolist(), "preds": preds.tolist()}


# Small convenience loader for typical project layout
def load_texts_from_csv(path: str, text_col: str = "full_text") -> List[str]:
    df = pd.read_csv(path)
    if text_col not in df.columns:
        # try common alternatives
        for alt in ["text", "content", "body"]:
            if alt in df.columns:
                text_col = alt
                break
    return df[text_col].fillna("").astype(str).tolist()
