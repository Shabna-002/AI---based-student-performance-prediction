@echo off
cd /d "%~dp0"
echo ========================================================
echo   EduPredict AI - Live Public Deployment Launcher
echo ========================================================
echo.
echo [1/2] Starting Flask Web Server...
start "" .\.venv\Scripts\python.exe app.py
timeout /t 2 /nobreak >nul
echo [2/2] Generating Public HTTPS Link via Cloudflare Tunnel...
echo.
echo --------------------------------------------------------
echo  Share the HTTPS URL generated below with anyone!
echo  (Keep this window open while you want the link active)
echo --------------------------------------------------------
echo.
.\cloudflared.exe tunnel --url http://127.0.0.1:5000
pause
