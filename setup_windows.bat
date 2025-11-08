@echo off
REM setup_windows.bat — Windows (Command Prompt)
python -m venv .venv
call .\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete. To run the app:
echo   call .\.venv\Scripts\activate
echo   python -m streamlit run app.py
pause
