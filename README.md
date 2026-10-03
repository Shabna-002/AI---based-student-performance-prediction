# EduPredict AI — Intelligent Student Performance Prediction & Academic Analytics

<div align="center">

![EduPredict AI Banner](https://img.shields.io/badge/EduPredict%20AI-v2.4%20Pro-38bdf8?style=for-the-badge&logo=probot&logoColor=white)
[![Live Demo](https://img.shields.io/badge/Live%20Platform-Render%20Cloud-00c7b7?style=for-the-badge&logo=render&logoColor=white)](https://ai-student-performance-qfua.onrender.com)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-8b5cf6?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Shabna-002/AI---based-student-performance-prediction)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%20WSGI-red?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![ML Library](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

**A Next-Generation Academic Intelligence Platform powered by Ensemble Machine Learning, 3D WebGL Visualization, and Real-Time Early Warning Intervention Triage.**

[🌐 Explore Live Demo](https://ai-student-performance-qfua.onrender.com) • [📖 Documentation](#-system-architecture) • [⚡ Quickstart](#-installation--setup) • [📊 Model Benchmarks](#-machine-learning-evaluation)

</div>

---

## 📌 Executive Summary

**EduPredict AI** is an enterprise-grade academic trajectory analytics and early intervention platform developed as an M.Tech CSE initiative. Traditional academic evaluations often identify struggling scholars after semester exams when it is too late for corrective interventions.

EduPredict AI bridges this institutional gap by leveraging an optimized **Random Forest Ensemble Classifier (97.5% Accuracy)** that evaluates multi-dimensional student telemetry—including attendance fidelity, internal assessment benchmarks, assignment submission rates, practical laboratory metrics, and backlog history—to predict final performance tiers and trigger proactive mentorship pathways in real time.

---

## 🌟 Key Platform Capabilities

### 1. 🤖 Multi-Factor Predictive Intelligence
- **Ensemble Inference**: Classifies student outcomes into distinct performance tiers (*High Performer*, *Average*, *Needs Attention / At-Risk*).
- **Risk Triage Engine**: Instant diagnostic flags detailing underlying academic vulnerabilities (e.g., attendance deficit, low assignment completion, practical lab distress).
- **Profile Presets**: One-click demo profiles (⭐ High Achiever, ⚠️ Borderline Average, 🚨 Critical Risk) for immediate institutional demonstrations.

### 2. 🔮 Interactive "What-If" Academic Studio
- Real-time parameter simulation sliders allowing mentors and students to evaluate hypothetical scenarios (e.g., *"If attendance increases by 15% and internal marks improve by 10 points, how does the final trajectory shift?"*).
- Instant asynchronous API recalculations without page reloading.

### 3. 📊 Institutional Performance Analytics Dashboard
- **Cohort Health Overview**: Real-time KPI counters tracking total enrolled scholars, cohort average GPA, at-risk percentage, and overall model accuracy.
- **Visual Telemetry**: Interactive Chart.js visual distributions including Risk Triage Doughnut charts and semester GPA progression curves.
- **Student Directory**: Instant client-side search, filtering, and record management with grade book integrations.

### 4. 🎨 Modern Cyber-Education UI with 3D Parallax
- **3D WebGL Spatial Universe**: Three.js dynamic neural network nodes and glowing academic mathematics glyphs floating with depth.
- **GPU-Accelerated Parallax Engine**: 60 FPS LERP (Linear Interpolation) cursor drift and scroll-driven perspective rotation.
- **Glassmorphism Architecture**: Frosted glass cards, glowing cyber-accents, dynamic SVG confidence gauges, and fully responsive layouts.

### 5. 🗄️ Resilient Dual-Database Architecture
- **Enterprise MySQL Production**: Normalized relational schema with foreign key integrity, prediction logs, and audit trails.
- **Zero-Config SQLite Cloud Fallback**: Automatically switches to local/cloud SQLite if MySQL credentials are not provisioned, ensuring 100% uptime on cloud hosts like Render.

---

## 📊 Machine Learning Evaluation & Benchmarks

The predictive engine was trained on a multi-variate academic dataset and evaluated against industry-standard classification models:

| Machine Learning Model | Classification Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Ensemble)** | **97.50%** | **97.55%** | **97.50%** | **0.9750** | 🏆 **Production Model** |
| **Logistic Regression** | 96.67% | 96.71% | 96.67% | 0.9668 | Baseline |
| **Decision Tree (CART)** | 96.25% | 96.31% | 96.25% | 0.9625 | Baseline |

### Input Features:
1. `Attendance` (% of lecture sessions attended)
2. `Internal_Marks` (Periodic assessment scores out of 50)
3. `Assignment_Score` (Cumulative coursework completion percentage)
4. `Study_Hours` (Weekly dedicated independent learning hours)
5. `Practical_Score` (Laboratory & applied technical evaluation)
6. `Past_Failures` (Historical backlogs or arrears count)

---

## 🛠️ Technology Stack

```text
Frontend:       HTML5 • Modern CSS3 • JavaScript (ES6+) • Bootstrap 5 • Three.js (WebGL) • Chart.js
Backend:        Python 3.10+ • Flask (WSGI Web Framework) • Gunicorn
Machine Learning: Scikit-Learn • Pandas • NumPy • Joblib
Databases:      MySQL Relational Database • SQLite3 (Self-healing cloud fallback)
DevOps / Cloud: Render Cloud Web Service • Git • Cloudflare Tunnel Integration
```

---

## 📂 Project Structure

```text
AI_Student_Performance_Prediction/
├── app.py                         # Core Flask application, routing & inference engine
├── requirements.txt               # Production Python dependencies
├── Procfile                       # Cloud WSGI deployment descriptor (Gunicorn)
├── runtime.txt                    # Python runtime specification for cloud builders
├── .env.example                   # Environment configuration blueprint
├── database/
│   ├── db.py                      # Dual-engine database abstraction (MySQL / SQLite)
│   └── student_performance.sql    # Relational database schema & seed records
├── ml/
│   ├── train_model.py             # Model training, cross-validation & benchmark pipeline
│   ├── student_performance.csv    # Academic dataset
│   └── student_performance_model.pkl # Serialized Random Forest classifier
├── static/
│   ├── css/
│   │   └── ai_futuristic_theme.css# Cyber-education dark blue/purple theme & glassmorphism
│   ├── js/
│   │   ├── parallax_engine.js     # 60 FPS LERP mouse parallax & 3D tilt engine
│   │   ├── three_education_bg.js  # Three.js WebGL neural nodes canvas
│   │   └── background_particles.js# Ambient 2D neural network particle mesh
│   ├── images/                    # UI branding assets & wide panoramic backgrounds
│   └── videos/                    # Optimized MP4 background video loop (9MB)
├── templates/
│   ├── base.html                  # Global layout with Three.js canvas & animated universe
│   ├── login.html                 # EduPredict AI portal authentication
│   ├── signup.html                # Faculty registration portal
│   ├── dashboard.html             # Performance Analytics & cohort triage
│   ├── students.html              # Student directory & real-time search
│   ├── predict.html               # Multi-factor prediction studio with SVG gauges
│   ├── what_if.html               # Interactive What-If simulation studio
│   └── student_profile.html       # Individual scholar trajectory dossier
└── reports/
    └── model_comparison.csv       # Benchmark metrics comparison export
```

---

## ⚡ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Shabna-002/AI---based-student-performance-prediction.git
cd AI---based-student-performance-prediction
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup (Optional)
The system is equipped with an automatic zero-config SQLite fallback. To utilize full MySQL:
```bash
mysql -u root -p < database/student_performance.sql
```
Create a `.env` file from `.env.example`:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=student_performance
SECRET_KEY=your_secret_key
```

### 5. Launch Application
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## ☁️ Live Cloud Deployment

This platform is configured for instant 24/7 cloud hosting on **Render**:
1. Connect this repository to your [Render Dashboard](https://dashboard.render.com).
2. Create a new **Web Service**.
3. Set the build command to: `pip install -r requirements.txt`
4. Set the start command to: `gunicorn app:app`

Live URL: **[https://ai-student-performance-qfua.onrender.com](https://ai-student-performance-qfua.onrender.com)**

---

## 👩‍💻 Author & Project Context

- **Academic Context**: M.Tech Computer Science & Engineering Microproject
- **Project Domain**: Artificial Intelligence in Education (AIEd) / Educational Data Mining (EDM)
- **Repository**: [Shabna-002/AI---based-student-performance-prediction](https://github.com/Shabna-002/AI---based-student-performance-prediction)

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
