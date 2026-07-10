import os
import joblib
import time
import json
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV

from utilities.logger import setup_logger

logger = setup_logger("train")

def train_models(X_train, y_train, models_dir: Path):
    """
    Trains Random Forest and XGBoost using RandomizedSearchCV for optimization.
    Saves the best models to models_dir.
    Returns the trained models and their cross-validation scores.
    """
    logger.info("Starting model training and hyperparameter optimization...")
    start_time_total = time.time()
    
    trained_models = {}
    
    # 1. Random Forest Optimization
    logger.info("--- Optimizing Random Forest ---")
    rf = RandomForestClassifier(random_state=42)
    rf_param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'criterion': ['gini', 'entropy']
    }
    
    t0 = time.time()
    # Using RandomizedSearchCV to keep it within reasonable time while still tuning
    rf_search = RandomizedSearchCV(rf, param_distributions=rf_param_grid, n_iter=5, cv=3, scoring='accuracy', random_state=42, n_jobs=-1)
    rf_search.fit(X_train, y_train)
    rf_train_time = time.time() - t0
    
    best_rf = rf_search.best_estimator_
    logger.info(f"Random Forest best parameters: {rf_search.best_params_}")
    logger.info(f"Random Forest best CV score: {rf_search.best_score_:.4f}")
    
    rf_model_path = models_dir / "RandomForest.pkl"
    joblib.dump(best_rf, rf_model_path)
    logger.info(f"Random Forest model saved to {rf_model_path}")
    
    trained_models["RandomForest"] = {
        "model": best_rf,
        "cv_score": rf_search.best_score_,
        "train_time": rf_train_time
    }
    
    # 2. XGBoost Optimization
    logger.info("--- Optimizing XGBoost ---")
    xgb_model = xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
    xgb_param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'gamma': [0, 0.1, 0.2],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }
    
    t0 = time.time()
    xgb_search = RandomizedSearchCV(xgb_model, param_distributions=xgb_param_grid, n_iter=5, cv=3, scoring='accuracy', random_state=42, n_jobs=-1)
    xgb_search.fit(X_train, y_train)
    xgb_train_time = time.time() - t0
    
    best_xgb = xgb_search.best_estimator_
    logger.info(f"XGBoost best parameters: {xgb_search.best_params_}")
    logger.info(f"XGBoost best CV score: {xgb_search.best_score_:.4f}")
    
    xgb_model_path = models_dir / "XGBoost.pkl"
    joblib.dump(best_xgb, xgb_model_path)
    logger.info(f"XGBoost model saved to {xgb_model_path}")
    
    trained_models["XGBoost"] = {
        "model": best_xgb,
        "cv_score": xgb_search.best_score_,
        "train_time": xgb_train_time
    }
    
    total_time = time.time() - start_time_total
    logger.info(f"All model training completed in {total_time:.2f} seconds.")
    
    return trained_models
