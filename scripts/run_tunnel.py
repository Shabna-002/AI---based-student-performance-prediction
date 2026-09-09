import subprocess
import time
import re
import sys
import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_EXE = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
if not os.path.exists(PYTHON_EXE):
    PYTHON_EXE = sys.executable

CLOUDFLARED_EXE = os.path.join(BASE_DIR, "cloudflared.exe")

print("Starting Flask application server...")
flask_proc = subprocess.Popen(
    [PYTHON_EXE, "app.py"],
    cwd=BASE_DIR,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
)

# Wait for Flask to become available
max_attempts = 15
ready = False
for i in range(max_attempts):
    time.sleep(1)
    try:
        req = urllib.request.urlopen("http://127.0.0.1:5000", timeout=2)
        if req.getcode() == 200:
            ready = True
            print("Flask server is up and responding at http://127.0.0.1:5000")
            break
    except Exception:
        continue

if not ready:
    print("Warning: Flask server did not respond within 15 seconds, proceeding anyway...")

print("Starting Cloudflare Tunnel to generate public HTTPS link...")
cloudflared_proc = subprocess.Popen(
    [CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:5000"],
    cwd=BASE_DIR,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

public_url = None
url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

for line in iter(cloudflared_proc.stdout.readline, ""):
    print(line, end="", flush=True)
    match = url_pattern.search(line)
    if match and not public_url:
        public_url = match.group(0)
        url_file = os.path.join(BASE_DIR, "public_url.txt")
        with open(url_file, "w") as f:
            f.write(public_url + "\n")
        print("\n" + "="*70)
        print("PUBLIC WORKING LINK GENERATED SUCCESSFULLY:")
        print(f"URL: {public_url}")
        print("="*70 + "\n", flush=True)

flask_proc.wait()
cloudflared_proc.wait()
