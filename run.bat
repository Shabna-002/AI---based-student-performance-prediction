@echo off
cd /d "%~dp0"
echo =========================================================
echo   AI Student Performance Prediction & Analytics System
echo =========================================================
echo.
echo Opening browser at http://127.0.0.1:5000/ ...
start http://127.0.0.1:5000/

if exist ".\.venv\Scripts\python.exe" (
    .\.venv\Scripts\python.exe app.py
) else if exist ".\venv\Scripts\python.exe" (
    .\venv\Scripts\python.exe app.py
) else (
    py app.py 2>nul || python app.py
)
pause
