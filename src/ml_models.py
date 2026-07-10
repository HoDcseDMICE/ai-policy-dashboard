import pandas as pd
import numpy as np
import logging
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

def setup_logger(log_file_path):
    # Create logger
    logger = logging.getLogger("ml_evaluator")
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
        
    # File handler
    fh = logging.FileHandler(log_file_path, mode='w')
    fh.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    return logger

def train_and_evaluate_models(data_path="data/merged_policy_data.csv", log_path="models/training.log"):
    """
    Trains XGBoost and Random Forest on the dataset, predicting 'is_policy_active' based on text.
    Returns the accuracy metrics and path to the log file.
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger = setup_logger(log_path)
    
    logger.info("Starting ML Evaluation process...")
    
    try:
        logger.info(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
        
        # We will predict 'is_policy_active' using 'full_text'
        if 'full_text' not in df.columns or 'is_policy_active' not in df.columns:
            logger.error("Required columns ('full_text', 'is_policy_active') not found in dataset.")
            return {"error": "Missing columns in data."}
            
        # Clean data
        df = df.dropna(subset=['full_text', 'is_policy_active'])
        
        # Ensure target is integer for XGBoost
        y = df['is_policy_active'].astype(int).values
        texts = df['full_text'].astype(str).values
        
        logger.info(f"Dataset loaded. Total valid samples: {len(y)}")
        
        # Feature extraction
        logger.info("Extracting TF-IDF features from text...")
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X = vectorizer.fit_transform(texts)
        
        # Train-test split
        logger.info("Splitting data into training and test sets (80/20)...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        results = {}
        
        # 1. Random Forest
        logger.info("--- Training Random Forest Classifier ---")
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        rf_preds = rf.predict(X_test)
        rf_acc = accuracy_score(y_test, rf_preds)
        logger.info(f"Random Forest Accuracy: {rf_acc:.4f}")
        logger.info(f"Random Forest Classification Report:\n{classification_report(y_test, rf_preds)}")
        results['Random Forest'] = {'accuracy': rf_acc}
        
        # 2. XGBoost
        logger.info("--- Training XGBoost Classifier ---")
        xgb_model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='logloss')
        xgb_model.fit(X_train, y_train)
        xgb_preds = xgb_model.predict(X_test)
        xgb_acc = accuracy_score(y_test, xgb_preds)
        logger.info(f"XGBoost Accuracy: {xgb_acc:.4f}")
        logger.info(f"XGBoost Classification Report:\n{classification_report(y_test, xgb_preds)}")
        results['XGBoost'] = {'accuracy': xgb_acc}
        
        logger.info("ML Evaluation process completed successfully.")
        
        return {
            "success": True,
            "metrics": results,
            "log_path": log_path
        }
        
    except Exception as e:
        logger.exception("An error occurred during model training.")
        return {"error": str(e)}

