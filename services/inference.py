import os
import joblib
import json
import time
from pathlib import Path
import numpy as np

from utilities.logger import setup_logger

logger = setup_logger("inference")
models_dir = Path(__file__).parent.parent / "models"

class ModelService:
    def __init__(self):
        self.models = {}
        self.vectorizer = None
        self.scaler = None
        self.encoder = None
        self.metadata = None
        self._load_resources()

    def _load_resources(self):
        try:
            meta_path = models_dir / "Metadata.json"
            if meta_path.exists():
                with open(meta_path, "r") as f:
                    self.metadata = json.load(f)
            
            vec_path = models_dir / "Vectorizer.pkl"
            if vec_path.exists():
                self.vectorizer = joblib.load(vec_path)
                
            scale_path = models_dir / "Scaler.pkl"
            if scale_path.exists():
                self.scaler = joblib.load(scale_path)
                
            rf_path = models_dir / "RandomForest.pkl"
            if rf_path.exists():
                self.models["RandomForest"] = joblib.load(rf_path)
                
            xgb_path = models_dir / "XGBoost.pkl"
            if xgb_path.exists():
                self.models["XGBoost"] = joblib.load(xgb_path)
                
            logger.info("Machine Learning models and resources loaded into memory successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML resources: {e}")

    def predict(self, text: str, document_length: int = 0):
        """
        Runs inference on new document text.
        """
        if not self.metadata or not self.vectorizer or not self.models:
            return {"error": "Models are not trained or loaded. Please train models first."}
            
        try:
            t0 = time.time()
            best_model_name = self.metadata["best_model"]
            model = self.models.get(best_model_name)
            
            if not model:
                return {"error": f"Best model '{best_model_name}' could not be loaded."}
            
            # Preprocess
            X_text = self.vectorizer.transform([text]).toarray()
            if self.scaler:
                num_scaled = self.scaler.transform([[document_length]])
                X = np.hstack((X_text, num_scaled))
            else:
                X = X_text
                
            # Predict
            pred = int(model.predict(X)[0])
            prob = float(model.predict_proba(X)[0][1])
            confidence = prob if pred == 1 else 1 - prob
            latency = time.time() - t0
            
            logger.info(f"Prediction complete. Label: {pred}, Confidence: {confidence:.2f}, Latency: {latency:.4f}s")
            
            return {
                "success": True,
                "prediction": "Active/Adopted" if pred == 1 else "Inactive/Draft",
                "probability": prob,
                "confidence": confidence,
                "algorithm_used": best_model_name,
                "prediction_latency_seconds": latency
            }
        except Exception as e:
            logger.exception("Prediction failed.")
            return {"error": str(e)}

# Singleton instance
inference_service = ModelService()
