import os
import shutil
import pandas as pd
from pathlib import Path
from typing import IO, Tuple


ALLOWED_EXT = {'.csv', '.json', '.xlsx', '.txt', '.zip', '.pdf', '.docx'}


def _secure_filename(name: str) -> str:
    return ''.join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()


def validate_extension(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXT


def ingest_file(uploaded_file: IO, filename: str, dest_dir: str = None) -> Tuple[bool, str]:
    """Save uploaded file safely, perform lightweight validation, and for tabular files
    return (success, message_or_path).

    Supports chunked reading for CSV via pandas when requested by downstream processors.
    """
    if dest_dir is None:
        dest_dir = str(Path(__file__).parent.parent / 'data' / 'uploads')
    os.makedirs(dest_dir, exist_ok=True)

    safe_name = _secure_filename(Path(filename).name)
    if not validate_extension(safe_name):
        return False, f"Unsupported file type: {Path(safe_name).suffix}"

    dest_path = Path(dest_dir) / safe_name
    # Stream copy to avoid large memory usage
    try:
        with open(dest_path, 'wb') as out_f:
            shutil.copyfileobj(uploaded_file, out_f)
    except Exception as e:
        return False, f"Failed to save uploaded file: {e}"

    # Quick validation for tabular files
    try:
        if dest_path.suffix.lower() == '.csv':
            # attempt to read just the header and a small sample
            for chunk in pd.read_csv(dest_path, chunksize=1000):
                # basic sanity: must have at least one column
                if chunk.shape[1] == 0:
                    return False, "CSV has no columns"
                break
        elif dest_path.suffix.lower() in ('.xlsx',):
            _ = pd.read_excel(dest_path, nrows=5)
        elif dest_path.suffix.lower() == '.json':
            _ = pd.read_json(dest_path, lines=False)
    except Exception as e:
        # remove corrupt file to avoid poisoning uploads
        try:
            dest_path.unlink()
        except Exception:
            pass
        return False, f"Uploaded file validation failed: {e}"

    return True, str(dest_path)
