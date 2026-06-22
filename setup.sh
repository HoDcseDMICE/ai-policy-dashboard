#!/bin/bash

# Setup script for AI Policy Trends Dashboard on Linux/macOS

echo ""
echo "=========================================================="
echo "AI Policy Trends Dashboard - Setup Script"
echo "=========================================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2)
echo "Found Python $python_version"

echo ""
echo "[1/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated"

echo ""
echo "[3/5] Installing dependencies..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed successfully"

echo ""
echo "[4/5] Downloading NLTK data..."
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')" > /dev/null 2>&1
echo "✓ NLTK data downloaded"

echo ""
echo "[5/5] Preprocessing data..."
python preprocess_data.py
if [ $? -ne 0 ]; then
    echo "WARNING: Data preprocessing failed"
    echo "If raw datasets are not available, the dashboard can still run using existing processed data in data/."
    echo "You can try running it manually: python preprocess_data.py"
fi

echo ""
echo "=========================================================="
echo "Setup completed successfully!"
echo "=========================================================="
echo ""
echo "Next steps:"
echo "1. Run the dashboard: streamlit run app.py"
echo "2. Open your browser: http://localhost:8501"
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
