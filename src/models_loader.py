import os
import pickle
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


def load_model_safe(name: str, models_dir: str = None) -> Optional[Any]:
    """Attempt to load a pickled model from models_dir/name.(pkl|joblib).
    Returns None on failure and logs an error. Use this to avoid crashes if
    model files are missing in production.
    """
    if models_dir is None:
        models_dir = str(Path(__file__).parent.parent / 'models')
    p = Path(models_dir)
    # try common extensions
    for ext in ('.pkl', '.joblib'):
        candidate = p / f"{name}{ext}"
        if candidate.exists():
            try:
                with open(candidate, 'rb') as f:
                    model = pickle.load(f)
                logger.info(f"Loaded model {candidate}")
                return model
            except Exception as e:
                logger.exception(f"Failed to load model {candidate}: {e}")
                return None
    logger.warning(f"Model {name} not found in {models_dir}")
    return None
