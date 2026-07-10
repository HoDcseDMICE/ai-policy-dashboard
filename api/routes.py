from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import json
from pathlib import Path
from datetime import datetime

from services.inference import inference_service
from ml.preprocess import load_and_preprocess_data
from training.train import train_models
from evaluation.evaluate import evaluate_models
from utilities.logger import get_system_logs

router = APIRouter(prefix="/api/model", tags=["Machine Learning"])

models_dir = Path(__file__).parent.parent / "models"
data_dir = Path(__file__).parent.parent / "data"

class PredictRequest(BaseModel):
    text: str
    document_length: int = 0

@router.get("/status")
def get_status():
    meta_path = models_dir / "Metadata.json"
    if meta_path.exists():
        with open(meta_path, "r") as f:
            metadata = json.load(f)
        return {"status": "trained", "metadata": metadata}
    return {"status": "untrained", "metadata": None}

@router.get("/evaluation")
def get_evaluation():
    meta_path = models_dir / "Metadata.json"
    if not meta_path.exists():
        raise HTTPException(status_code=404, detail="Models not trained yet.")
    with open(meta_path, "r") as f:
        return json.load(f)

@router.get("/logs")
def get_logs():
    return {"logs": get_system_logs()}

@router.post("/predict")
def predict(request: PredictRequest):
    result = inference_service.predict(request.text, request.document_length)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

def retrain_task():
    try:
        X_train, X_test, y_train, y_test = load_and_preprocess_data(data_dir, models_dir)
        if X_train is not None:
            models_dict = train_models(X_train, y_train, models_dir)
            evaluate_models(models_dict, X_test, y_test, models_dir, inference_service.vectorizer)
            # Reload resources into memory
            inference_service._load_resources()
    except Exception as e:
        import logging
        logging.getLogger("train").error(f"Retrain task failed: {e}")

@router.post("/retrain")
def retrain_models(background_tasks: BackgroundTasks):
    background_tasks.add_task(retrain_task)
    return {"status": "Training started in background."}
