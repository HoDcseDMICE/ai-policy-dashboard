"""
Generate a reusable access code for secure local launches of the dashboard.
Writes the code to `scripts/access_code.txt` and prints it.
Usage:
    python scripts/generate_access_code.py
"""
import uuid
from pathlib import Path

OUT = Path(__file__).parent / 'access_code.txt'
code = f"AI-DASH-2026-{uuid.uuid4().hex[:6].upper()}"
OUT.write_text(code)
print('Access code generated and saved to', OUT)
print('Access code:', code)
