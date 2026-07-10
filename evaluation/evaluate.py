import json
import time
import numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import joblib

from utilities.logger import setup_logger

logger = setup_logger("evaluate")

def evaluate_models(models_dict, X_test, y_test, models_dir: Path, vectorizer=None):
    """
    Evaluates trained models and saves metrics to models/Metadata.json.
    """
    logger.info("Evaluating models on test dataset...")
    metrics_summary = {}
    
    for name, data in models_dict.items():
        model = data["model"]
        
        t0 = time.time()
        preds = model.predict(X_test)
        inference_time = time.time() - t0
        
        try:
            preds_proba = model.predict_proba(X_test)[:, 1]
            roc_auc = float(roc_auc_score(y_test, preds_proba))
        except:
            roc_auc = 0.0
            
        acc = float(accuracy_score(y_test, preds))
        prec = float(precision_score(y_test, preds, zero_division=0))
        rec = float(recall_score(y_test, preds, zero_division=0))
        f1 = float(f1_score(y_test, preds, zero_division=0))
        cm = confusion_matrix(y_test, preds).tolist()
        
        # Feature Importance
        feat_importance = []
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            if vectorizer and len(importances) >= len(vectorizer.get_feature_names_out()):
                names = vectorizer.get_feature_names_out()
                # Get top 15 features
                indices = np.argsort(importances[:len(names)])[::-1][:15]
                for i in indices:
                    feat_importance.append({
                        "feature": str(names[i]),
                        "importance": float(importances[i])
                    })
        
        metrics_summary[name] = {
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1_Score": f1,
            "ROC_AUC": roc_auc,
            "ConfusionMatrix": cm,
            "InferenceTime": inference_time,
            "TrainTime": data["train_time"],
            "CrossValidationScore": data["cv_score"],
            "FeatureImportance": feat_importance
        }
        logger.info(f"{name} Evaluation -> Accuracy: {acc:.4f}, ROC_AUC: {roc_auc:.4f}")

    # Select best model based on F1 Score
    best_model_name = max(metrics_summary.keys(), key=lambda k: metrics_summary[k]["F1_Score"])
    logger.info(f"Automatically selected best model: {best_model_name}")
    
    metadata = {
        "last_training_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "best_model": best_model_name,
        "metrics": metrics_summary
    }
    
    metadata_path = models_dir / "Metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)
        
    logger.info(f"Saved evaluation metrics to {metadata_path}")
    return metadata
