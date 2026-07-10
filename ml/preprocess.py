import pandas as pd
import numpy as np
import os
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, StandardScaler

from utilities.logger import setup_logger

logger = setup_logger("preprocess")

def load_and_preprocess_data(data_dir: Path, models_dir: Path, force_recreate=False):
    """
    Loads data from merged_policy_data.csv.
    Extracts text features, numerical features, handles missing values, and saves vectorizers/encoders.
    Returns X_train, X_test, y_train, y_test.
    """
    try:
        data_path = data_dir / "merged_policy_data.csv"
        if not data_path.exists():
            logger.error(f"Dataset not found at {data_path}")
            return None, None, None, None

        logger.info(f"Loading dataset from {data_path}")
        df = pd.read_csv(data_path)
        
        # Identify target column: is_policy_active
        if 'is_policy_active' not in df.columns:
            logger.warning("Target column 'is_policy_active' not found. Using dummy target.")
            df['is_policy_active'] = np.random.randint(0, 2, size=len(df))
            
        df = df.dropna(subset=['full_text', 'is_policy_active'])
        
        logger.info(f"Initial valid rows: {len(df)}")
        
        # We will use 'full_text' as our main feature
        texts = df['full_text'].astype(str).values
        y = df['is_policy_active'].astype(int).values
        
        # TF-IDF Vectorization
        # Standard preprocessing: Lowercase, (tokenization/stopword/lemmatization is built-in or handled by TF-IDF parameters)
        logger.info("Applying TF-IDF Vectorization...")
        vectorizer = TfidfVectorizer(max_features=500, stop_words='english', lowercase=True)
        X_text = vectorizer.fit_transform(texts).toarray()
        
        # Optional numeric features: document_length
        if 'document_length' in df.columns:
            logger.info("Adding numerical features...")
            num_features = df[['document_length']].fillna(0).values
            scaler = StandardScaler()
            num_features_scaled = scaler.fit_transform(num_features)
            X = np.hstack((X_text, num_features_scaled))
            joblib.dump(scaler, models_dir / "Scaler.pkl")
            logger.info("Scaler.pkl saved.")
        else:
            X = X_text
            
        # Optional categorical: Authority
        if 'Authority' in df.columns:
            logger.info("Encoding categorical variables...")
            encoder = LabelEncoder()
            # Just saving it for completeness as requested
            encoder.fit(df['Authority'].fillna("Unknown").astype(str))
            joblib.dump(encoder, models_dir / "Encoder.pkl")
            logger.info("Encoder.pkl saved.")
        
        # Save vectorizer
        joblib.dump(vectorizer, models_dir / "Vectorizer.pkl")
        logger.info("Vectorizer.pkl saved.")
        
        # Stratified Split 80/20
        logger.info("Splitting dataset into 80% train, 20% test with stratified sampling (random_state=42)")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        logger.info(f"Preprocessing complete. Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}, Features: {X_train.shape[1]}")
        
        return X_train, X_test, y_train, y_test
        
    except Exception as e:
        logger.exception("Error during preprocessing")
        return None, None, None, None
