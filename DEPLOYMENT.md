# 🚀 Complete Deployment Guide: AI-Based Student Performance Prediction

This guide provides step-by-step instructions for all available deployment methods, ranging from instant 1-click sharing to 24/7 cloud hosting and containerization.

---

## 🧭 Deployment Method Quick Selector

| Method | Best For | Cost | Setup Time | Needs GitHub? |
|---|---|---|---|---|
| **1. Hugging Face Spaces** | ML projects, permanent cloud link | **Free** | 3 mins | Yes |
| **2. Cloudflare Tunnel (`share_online.bat`)** | Instant public link from your PC | **Free** | 10 seconds | No |
| **3. Local Wi-Fi / LAN** | Classroom / Viva demo on phone or laptop | **Free** | Instant | No |
| **4. Render** | 24/7 Production Web Service | **Free Tier** | 3 mins | Yes |
| **5. Railway** | Fast cloud hosting with DB | **Free / Trial** | 2 mins | Yes |
| **6. PythonAnywhere** | Python-specific hosting with MySQL | **Free Tier** | 5 mins | Yes |
| **7. Docker / Docker Compose** | AWS / GCP / Azure / Any Cloud VPS | Standard VPS | 1 command | No |
| **8. Vercel** | Serverless Python hosting | **Free Tier** | 2 mins | Yes |

---

## ⚡ Method 1: Instant Public Live Sharing (Cloudflare Tunnel)

> [!TIP]
> **No accounts, no credit cards, and no cloud setup needed!** Runs directly from your computer and generates a live `https://*.trycloudflare.com` URL accessible anywhere worldwide.

1. Double-click **`share_online.bat`** in the project folder (or run `.\share_online.bat` in terminal).
2. It starts Flask and opens a secure Cloudflare HTTPS tunnel.
3. Copy the generated URL (e.g. `https://random-words.trycloudflare.com`) and open it in any browser or share it.

---

## 📶 Method 2: Local Wi-Fi / LAN Sharing (Classroom / Lab Demo)

> [!NOTE]
> Perfect for demonstrating the project to an examiner, professor, or friend on their phone or laptop without needing cloud accounts.

1. Start the Flask application:
   ```bash
   .\.venv\Scripts\python.exe app.py
   ```
2. Connect your phone or other device to the **same Wi-Fi network**.
3. Open the browser on your phone or other device and visit:
   ```
   http://<YOUR_LOCAL_IP>:5000
   ```
   *(On this machine, your current Wi-Fi IP is: `http://10.169.225.222:5000`)*

---

## 🤗 Method 3: Hugging Face Spaces (100% Free AI/ML Cloud Hosting)

Hugging Face Spaces is designed specifically for machine learning and AI applications and is permanently free.

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and log in.
2. Click **Create new Space**.
3. Fill in:
   - **Space name**: `student-performance-ai`
   - **License**: `mit`
   - **Space SDK**: Select **Docker** (Blank)
   - **Space hardware**: `Free - 2 vCPU, 16GB RAM`
4. Under your new Space repository, upload the project files or push via Git:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/student-performance-ai
   git push hf main
   ```
5. Hugging Face will automatically read the provided [Dockerfile](file:///c:/Users/HP/Downloads/AI_Student_Performance_Prediction_MTech_Microproject%20(1)/Dockerfile) and launch your live app with a public `https://*.hf.space` link!

---

## 🌟 Method 4: Deploy to Render (24/7 Free Web Service)

[Render](https://render.com) offers free web hosting with automatic continuous deployment from GitHub.

### Step 1: Push Changes to GitHub
```bash
git add .
git commit -m "Add Docker and multi-cloud deployment configs"
git push origin main
```

### Step 2: Create Web Service on Render
1. Go to [dashboard.render.com](https://dashboard.render.com) and log in.
2. Click **New +** → **Web Service**.
3. Select your GitHub repository: `Shabna-002/AI---based-student-performance-prediction`.
4. Render will detect the pre-configured [render.yaml](file:///c:/Users/HP/Downloads/AI_Student_Performance_Prediction_MTech_Microproject%20%281%29/render.yaml) automatically, or configure:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --workers 2 --timeout 120`
   - **Instance Type**: `Free`
5. Add Environment Variables:
   - `SECRET_KEY` = `(generate any random string)`
   - `DB_ENGINE` = `sqlite`
6. Click **Deploy Web Service**. Your live site will be available at `https://<service-name>.onrender.com`.

---

## 🚂 Method 5: Deploy to Railway

1. Go to [railway.app](https://railway.app) and log in with GitHub.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select `AI---based-student-performance-prediction`.
4. Railway automatically reads [railway.json](file:///c:/Users/HP/Downloads/AI_Student_Performance_Prediction_MTech_Microproject%20%281%29/railway.json) and deploys your service.
5. In project settings, click **Generate Domain** to get your public `.up.railway.app` URL.

---

## 🐍 Method 6: Deploy to PythonAnywhere

1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Open a **Bash** console:
   ```bash
   git clone https://github.com/Shabna-002/AI---based-student-performance-prediction.git
   cd AI---based-student-performance-prediction
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Go to the **Web** tab:
   - Click **Add a new web app** → **Manual Configuration** → **Python 3.10**.
   - Path: `/home/yourusername/AI---based-student-performance-prediction`
   - Virtualenv: `/home/yourusername/AI---based-student-performance-prediction/venv`
4. Set WSGI configuration file:
   ```python
   import sys, os
   path = '/home/yourusername/AI---based-student-performance-prediction'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
5. Click **Reload** to go live at `https://yourusername.pythonanywhere.com`.

---

## 🐳 Method 7: Docker & Docker Compose (Cloud VPS / Local Container)

Deploy on any machine or VPS (AWS EC2, Google Compute Engine, DigitalOcean Droplet, Linode):

```bash
# Build and run with Docker
docker build -t student-ai-app .
docker run -d -p 5000:7860 --name student-ai student-ai-app

# Or with Docker Compose:
docker compose up -d
```
Access at `http://localhost:5000` or `http://<SERVER_IP>:5000`.

---

## ▲ Method 8: Deploy to Vercel (Serverless)

With the pre-configured [vercel.json](file:///c:/Users/HP/Downloads/AI_Student_Performance_Prediction_MTech_Microproject%20%281%29/vercel.json):
1. Install Vercel CLI: `npm i -g vercel` (or connect your repo on [vercel.com](https://vercel.com)).
2. In the project folder, run:
   ```bash
   vercel
   ```
3. Follow the prompt to deploy directly to Vercel serverless.

---

## 🔐 Default Login Credentials

Across all deployment methods:
- **Username**: `admin`
- **Password**: `admin123`
