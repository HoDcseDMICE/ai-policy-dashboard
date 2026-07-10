import logging
import os
from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).parent.parent / "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = LOG_DIR / "application.log"

def setup_logger(name: str) -> logging.Logger:
    """Sets up a standardized logger for the Polaris AI application."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to prevent duplicates
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(LOG_FILE, mode='a')
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatting
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger

def get_system_logs() -> list:
    """Reads and parses the application log file."""
    logs = []
    if not LOG_FILE.exists():
        return logs
        
    with open(LOG_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" - ")
            if len(parts) >= 4:
                timestamp = parts[0]
                module = parts[1]
                level = parts[2]
                message = " - ".join(parts[3:])
                logs.append({
                    "timestamp": timestamp,
                    "module": module,
                    "level": level,
                    "message": message
                })
    # Return reversed to show newest first
    return logs[::-1]

def clear_system_logs() -> bool:
    """Clears the application log file."""
    try:
        with open(LOG_FILE, "w") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - system_logger - INFO - Logs cleared by admin.\n")
        return True
    except Exception:
        return False
