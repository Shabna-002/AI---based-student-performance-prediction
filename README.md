# AI-Based Student Performance Prediction and Database Management System
**M.Tech CSE Project**

An end-to-end intelligent web application that predicts student academic performance using machine learning algorithms (Random Forest, Decision Tree, Logistic Regression) combined with a relational database (MySQL) and a Flask web interface.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Active%20Public%20Link-success?style=for-the-badge&logo=cloudflare)](https://female-transcription-villas-paragraphs.trycloudflare.com)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/Shabna-002/AI---based-student-performance-prediction)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Shabna-002/AI---based-student-performance-prediction)

### 🌐 Live Public Link:
👉 **[Open Live EduPredict AI Application](https://female-transcription-villas-paragraphs.trycloudflare.com)**  
* **Default Username:** `admin`  
* **Default Password:** `admin123`  

---

## 🚀 Features
- **Student Performance Prediction**: Predicts student success levels based on attendance, internal marks, assignments, failures, and GPA.
- **Machine Learning Models**: Compares Logistic Regression, Decision Tree, and Random Forest models with evaluation metrics (Accuracy, Precision, Recall, F1-Score).
- **Database Management System**: Structured MySQL database for managing students, subjects, marks, attendance, and prediction logs.
- **Web Dashboard & Reports**: Interactive web UI built with Flask & Bootstrap, featuring student records management, dynamic prediction forms, and downloadable reports.

---

## 📁 Project Structure
```text
├── app.py                     # Main Flask web application
├── requirements.txt           # Python dependencies
├── .env.example               # Environment configuration template
├── run.bat                    # Windows one-click local launcher
├── share_online.bat           # Cloudflare Tunnel public preview launcher
├── database/
│   └── student_performance.sql # MySQL database schema & initial seed data
├── ml/
│   ├── train_model.py         # Model training & comparison script
│   ├── student_performance.csv# Training dataset
│   └── student_performance_model.pkl # Trained Random Forest model
├── reports/                   # Documentation, presentation & reports
├── templates/                 # HTML templates (Flask/Jinja2)
└── scripts/                   # Utility scripts
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.10 or higher
- MySQL Server (e.g. MySQL Community Server or XAMPP)
- Git

### 2. Database Setup
1. Start your MySQL service.
2. Import the schema and seed data into MySQL:
   ```bash
   mysql -u root -p < database/student_performance.sql
   ```

### 3. Environment Configuration
Copy `.env.example` to `.env` and set your MySQL credentials:
```bash
cp .env.example .env
```
Inside `.env`:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=student_performance
SECRET_KEY=your_secret_key_here
```

### 4. Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 5. Train Machine Learning Models (Optional)
The pre-trained model is already included in `ml/student_performance_model.pkl`. To retrain or evaluate:
```bash
python ml/train_model.py
```

### 6. Run Application
```bash
python app.py
```
Open your browser and navigate to: **http://127.0.0.1:5000/**

**Default Admin Credentials:**
- **Username**: `admin`
- **Password**: `admin123`

---

## 🌐 Public Tunnel / Sharing
To share the running app publicly over an encrypted HTTPS link, execute:
```bash
share_online.bat
```
*(Requires `cloudflared.exe`)*

---

## ☁️ 24/7 Cloud Deployment (Render / Railway / PythonAnywhere)
The project is configured for cloud deployment with Gunicorn WSGI and automatic dual-database support (MySQL with SQLite zero-config fallback).

For step-by-step instructions on deploying to **Render**, **Railway**, or **PythonAnywhere**, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 📝 Note
The included CSV is synthetic demonstration data. Replace it with approved real academic data before publishing or reporting research results.

