@echo off
REM Setup script for AI Policy Trends Dashboard on Windows

echo.
echo ============================================================
echo AI Policy Trends Dashboard - Setup Script
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    exit /b 1
)

echo [1/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo [3/5] Installing dependencies...
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed successfully

echo.
echo [4/5] Downloading NLTK data...
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')" >nul 2>&1
echo ✓ NLTK data downloaded

echo.
echo [5/5] Preprocessing data...
python preprocess_data.py
if errorlevel 1 (
    echo WARNING: Data preprocessing failed
    echo You can try running it manually: python preprocess_data.py
)

echo.
echo ============================================================
echo Setup completed successfully!
echo ============================================================
echo.
echo Next steps:
echo 1. Run the dashboard: streamlit run app.py
echo 2. Open your browser: http://localhost:8501
echo.
echo If raw datasets are not installed, the app can still use existing processed data in data\
exiting.
echo.
echo To activate the environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
pause
