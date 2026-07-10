import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from ml.preprocess import load_and_preprocess_data
from training.train import train_models
from evaluation.evaluate import evaluate_models
import joblib

if __name__ == "__main__":
    data_dir = Path("data")
    models_dir = Path("models")
    print("Starting initial FYP ML Training Pipeline...")
    X_train, X_test, y_train, y_test = load_and_preprocess_data(data_dir, models_dir)
    if X_train is not None:
        print("Preprocessing done. Training models...")
        models_dict = train_models(X_train, y_train, models_dir)
        vec = joblib.load(models_dir / "Vectorizer.pkl")
        print("Training done. Evaluating...")
        evaluate_models(models_dict, X_test, y_test, models_dir, vec)
        print("Pipeline execution complete! Models and metrics saved.")
    else:
        print("Failed to load or preprocess data.")
