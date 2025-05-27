@echo off
SETLOCAL

IF NOT EXIST "venv\" (
    python -m venv venv
)

CALL venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python src\main.py

ENDLOCAL