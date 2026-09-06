# 🚀 Cloud Deployment Guide

This guide provides step-by-step instructions to deploy the **AI-Based Student Performance Prediction and Database Management System** to 24/7 cloud hosting platforms.

---

## 📋 Overview of Changes for Cloud Readiness

1. **Production WSGI Server**: Configured `gunicorn` in `requirements.txt` and `Procfile`.
2. **Dual Database Engine**:
   - **Zero-Config SQLite Fallback**: Automatically creates database tables and the default `admin` account if no external MySQL database is provided.
   - **Cloud MySQL Support**: Seamlessly connects to any remote MySQL database (e.g. Aiven, TiDB Cloud, Clever Cloud, Railway MySQL) if `DB_HOST`, `DB_USER`, `DB_PASSWORD`, etc. are set.
3. **Dynamic Port Binding**: Application automatically reads the `PORT` assigned by cloud providers.
4. **Cloud Configurations**: Pre-configured `render.yaml`, `railway.json`, and `runtime.txt`.

---

## 🌟 Method 1: Deploy to Render (Recommended - Free Tier)

[Render](https://render.com) offers free web service hosting for Python web applications.

### Step 1: Push Changes to GitHub
Open your terminal or Git bash and push the new deployment files to GitHub:
```bash
git add .
git commit -m "Configure production WSGI and cloud deployment files"
git push origin main
```

### Step 2: Create a Web Service on Render
1. Go to [dashboard.render.com](https://dashboard.render.com) and log in.
2. Click **New +** and select **Web Service**.
3. Under **Connect a repository**, select your repository:
   `Shabna-002/AI---based-student-performance-prediction`
4. Render will automatically detect settings, or fill them in as follows:
   - **Name**: `student-performance-ai` (or your choice)
   - **Region**: Closest to you (e.g., *Singapore*, *Frankfurt*, *Oregon*)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --workers 2 --timeout 120`
   - **Instance Type**: `Free`

### Step 3: Configure Environment Variables
Under the **Environment Variables** section, add:
- `SECRET_KEY` = `(click 'Generate' or enter any random string)`
- `DB_ENGINE` = `sqlite` *(Default zero-config mode)*

> [!TIP]
> **Using Cloud MySQL on Render (Optional):**
> If you prefer using an external MySQL database instead of SQLite:
> 1. Create a free MySQL database on [Aiven.io](https://aiven.io) or [TiDB Cloud](https://tidbcloud.com).
> 2. Add `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT` in Render's environment variables.
> 3. Import `database/student_performance.sql` into that database.

### Step 4: Deploy
Click **Deploy Web Service**. Within 2-3 minutes, your application will be live at:
`https://your-service-name.onrender.com`

---

## 🚂 Method 2: Deploy to Railway

[Railway](https://railway.app) supports automatic deployments with Nixpacks.

### Step 1: Deploy from GitHub
1. Go to [railway.app](https://railway.app) and sign in with GitHub.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select `AI---based-student-performance-prediction`.
4. Railway will automatically detect `railway.json` and `Procfile`.

### Step 2: (Optional) Add MySQL Database on Railway
1. In the Railway project dashboard, click **New** → **Database** → **Add MySQL**.
2. Railway will provision a MySQL instance and provide connection variables.
3. Link the MySQL environment variables (`MYSQLHOST`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`, `MYSQLPORT`) to your web service.

---

## 🐍 Method 3: Deploy to PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com) provides free Python web hosting with built-in MySQL support.

1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Go to the **Consoles** tab and start a **Bash** console.
3. Clone your repository:
   ```bash
   git clone https://github.com/Shabna-002/AI---based-student-performance-prediction.git
   cd AI---based-student-performance-prediction
   ```
4. Create and activate a virtualenv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Go to the **Web** tab:
   - Click **Add a new web app**.
   - Choose **Manual Configuration** → **Python 3.10** (or 3.11).
   - Set **Source code** path: `/home/yourusername/AI---based-student-performance-prediction`
   - Set **Virtualenv** path: `/home/yourusername/AI---based-student-performance-prediction/venv`
6. Edit the **WSGI configuration file** (link provided on the Web tab) to load Flask:
   ```python
   import sys
   import os

   path = '/home/yourusername/AI---based-student-performance-prediction'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```
7. Click **Reload yourusername.pythonanywhere.com** and view your live site!

---

## ⚡ Default Admin Credentials

Regardless of platform, the default credentials are:
- **Username**: `admin`
- **Password**: `admin123`

