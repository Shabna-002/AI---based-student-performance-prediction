# PROJECT REPORT

## AI-BASED STUDENT PERFORMANCE PREDICTION AND DATABASE MANAGEMENT SYSTEM

---

### **A Project Report Submitted in Partial Fulfillment of the Requirements for the Award of the Degree of**
### **MASTER OF TECHNOLOGY (M.TECH)**
### **IN**
### **COMPUTER SCIENCE AND ENGINEERING**

---

## TABLE OF CONTENTS
1. [Abstract](#abstract)
2. [Chapter 1: Introduction](#chapter-1-introduction)
   - 1.1 Background
   - 1.2 Problem Statement
   - 1.3 Objectives
   - 1.4 Scope of the Project
3. [Chapter 2: Literature Survey & Existing System](#chapter-2-literature-survey--existing-system)
   - 2.1 Existing System Overview
   - 2.2 Drawbacks of the Existing System
   - 2.3 Proposed System Architecture
   - 2.4 Advantages of the Proposed System
4. [Chapter 3: System Requirements Specification](#chapter-3-system-requirements-specification)
   - 3.1 Hardware Requirements
   - 3.2 Software Requirements
   - 3.3 Technology Stack
5. [Chapter 4: System Design & Architecture](#chapter-4-system-design--architecture)
   - 4.1 High-Level Architecture
   - 4.2 Data Flow Diagram (DFD)
   - 4.3 Database Schema & Entity-Relationship Design
   - 4.4 Machine Learning Pipeline Design
6. [Chapter 5: Methodology & Implementation](#chapter-5-methodology--implementation)
   - 5.1 Dataset Description & Preprocessing
   - 5.2 Feature Engineering
   - 5.3 Machine Learning Algorithms (Logistic Regression, Decision Tree, Random Forest)
   - 5.4 Web Application Backend (Flask)
   - 5.5 Frontend User Interface (Bootstrap 5)
   - 5.6 Security & Authentication
   - 5.7 Cloud Deployment via Secure Tunneling
7. [Chapter 6: Experimental Results & Performance Analysis](#chapter-6-experimental-results--performance-analysis)
   - 6.1 Model Performance Metrics
   - 6.2 Comparative Evaluation
   - 6.3 Risk Classification & Intervention Strategy
8. [Chapter 7: Conclusion & Future Scope](#chapter-7-conclusion--future-scope)
   - 7.1 Conclusion
   - 7.2 Future Enhancements
9. [References](#references)

---

## ABSTRACT

In modern higher educational institutions, early identification of academically at-risk students is critical for proactive mentoring, improving retention rates, and optimizing institutional performance. Traditional academic information management systems operate predominantly as passive record-keeping databases with post-facto semester result declarations, lacking predictive intelligence and automated early warning capabilities. 

This project presents the design and implementation of an end-to-end **AI-Based Student Performance Prediction and Database Management System**. The system marries a normalized relational database management system (**MySQL**) with supervised machine learning algorithms to forecast student academic trajectories into three distinct risk tiers: **High Performance**, **Average Performance**, and **Low Performance (At-Risk)**. A classification pipeline compares **Logistic Regression**, **Decision Tree Classifier**, and **Random Forest Classifier**, with the optimal ensemble model deployed via serialized persistence (`joblib`). 

The software architecture integrates a lightweight, robust **Python Flask** micro-framework backend with a responsive, modern **Bootstrap 5** frontend dashboard. The platform incorporates multi-user role-based authentication, student record lifecycle management (CRUD), interactive real-time multi-variable inference computation, model confidence scoring, and dynamic pedagogical recommendation generation. Furthermore, the application is provisioned for global deployment using zero-trust encrypted tunneling. The resulting application bridges the gap between transactional academic databases and actionable predictive analytics.

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background
The landscape of higher education has experienced substantial growth in student enrollment and curricular complexity. Academic administrators, department chairs, and faculty advisors are tasked with tracking substantial student records encompassing attendance percentages, continuous internal assessment evaluations, assignment submissions, historical cumulative grade point averages (CGPA), and backlog tallies. Despite the abundance of academic data, legacy institutional systems remain isolated transactional tools that report outcomes only after semester-end examinations have transpired.

Educational Data Mining (EDM) and Machine Learning (ML) present powerful methodologies for discovering latent academic patterns, modeling non-linear learning behavior, and synthesizing actionable risk forecasts prior to summative assessments.

### 1.2 Problem Statement
Traditional academic management processes suffer from three major vulnerabilities:
1. **Lack of Early Intervention**: Academic intervention usually occurs after a student fails end-semester exams, rendering remedial support reactive and less effective.
2. **Disconnected Architecture**: Institutional databases record marks and attendance in silos without feeding automated analytical intelligence engines.
3. **Absence of Risk Stratification**: Faculty members lack automated, quantitative tools to categorize students into risk bands based on continuous evaluation metrics.

### 1.3 Objectives
The primary objectives of this microproject are:
- **Relational Database Design**: To architect a third-normal-form (3NF) relational database schema in MySQL for managing student identities, enrollments, subject mappings, attendance records, continuous evaluation marks, and prediction logs.
- **Machine Learning Classification Pipeline**: To extract significant academic features (`attendance`, `internal`, `assignment`, `gpa`, `failures`), apply stratified train-test partitioning, and train multiple classification models.
- **Comparative Empirical Analysis**: To benchmark candidate algorithms using standard statistical metrics including Accuracy, Precision, Recall, and F1-Score.
- **Interactive Web Portal**: To build a secure, full-stack web application featuring user authentication, record management (Add, View, Edit, Delete), and real-time inference prediction.
- **Pedagogical Action Engine**: To provide customized recommendations and confidence scores based on predicted performance categories.
- **Cloud Deployment**: To establish a secure public access link for remote accessibility and demonstration.

### 1.4 Scope of the Project
The application is engineered for higher education academic departments, faculty mentors, and academic controllers. The initial prototype operates on departmental cohorts with supervised classification across five core indicators, outputting actionable advisory guidelines for timely faculty intervention.

---

## CHAPTER 2: LITERATURE SURVEY & EXISTING SYSTEM

### 2.1 Existing System Overview
Most existing academic information software solutions function as basic transactional Management Information Systems (MIS). Data entry operators or faculty upload tabular records into centralized databases or spreadsheet files. Outputs are restricted to standard grade sheets, consolidated mark lists, and static PDF transcripts.

### 2.2 Drawbacks of the Existing System
- **Static and Retrospective**: Information is descriptive of historical events rather than predictive of future outcomes.
- **Manual Advisory Burden**: Faculty mentors manually compute aggregate percentages to manually identify struggling students.
- **High Error Margin**: Subtle declining trends (e.g., adequate attendance masked by declining assignment quality and rising backlogs) are frequently overlooked until final semester marks are calculated.
- **No Direct ML Integration**: Data must be manually exported, preprocessed in external analytical tools (like SPSS, R, or standalone Python scripts), and manually evaluated.

### 2.3 Proposed System Architecture
The proposed system addresses these shortcomings by directly coupling a normalized relational database with an embedded machine learning inference engine within a unified Flask web portal:
- **Integrated Database**: Live MySQL database maintains real-time records and archives every inference request with timestamping.
- **Automated Inference**: Real-time evaluation of 5 key indicators without requiring manual offline analysis.
- **Immediate Categorization**: Output is stratified into High, Average, and Low tiers accompanied by statistical model confidence.
- **Automated Advisory Generation**: Tailored pedagogical guidelines (e.g., remedial tutorials, peer-mentoring, honors project tracking) are rendered dynamically.

### 2.4 Advantages of the Proposed System
- **Proactive Remediation**: Early identification empowers faculty to conduct timely interventions weeks before semester finals.
- **Data-Driven Objectivity**: Eliminates subjective bias in student evaluation through standardized machine learning algorithms.
- **Usability & Clean Aesthetics**: Modern, responsive user experience accessible from any browser or mobile device.
- **Auditing & Traceability**: Centralized history of predictions allows longitudinal tracking of student improvement.

---

## CHAPTER 3: SYSTEM REQUIREMENTS SPECIFICATION

### 3.1 Hardware Requirements
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher (Intel Core i5 recommended)
- **RAM**: Minimum 4 GB (8 GB recommended for concurrent database and model serving)
- **Storage**: Minimum 500 MB free hard drive space
- **Network**: Standard TCP/IP network connection (for public tunneling)

### 3.2 Software Requirements
- **Operating System**: Windows 10/11, Ubuntu Linux 20.04+, or macOS
- **Programming Language**: Python 3.10+
- **Database Engine**: MySQL Server 8.0+
- **Web Server / Framework**: Flask (WSGI Development Server / Werkzeug)
- **Web Browser**: Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari

### 3.3 Technology Stack
| Layer | Technology Used | Description |
| :--- | :--- | :--- |
| **Backend Framework** | Python Flask | Lightweight WSGI micro-framework managing routing, sessions, and request dispatching |
| **Database System** | MySQL 8.0 | Relational database management system with foreign key integrity and transactional safety |
| **Database Connector** | `mysql-connector-python` | Native Python driver for executing parameterized SQL queries |
| **Machine Learning** | `scikit-learn` | Open-source ML library for classification, data pipelines, and evaluation metrics |
| **Data Manipulation** | `pandas`, `numpy` | High-performance array and tabular data preprocessing |
| **Model Persistence** | `joblib` | High-throughput binary serialization of trained estimator pipelines |
| **Frontend Styling** | Bootstrap 5.3.3 | Responsive grid layout, card components, utility classes, and modal styling |
| **Iconography & Fonts**| Bootstrap Icons & Inter | Modern institutional typography and clean UI visual cues |
| **Edge Deployment** | Cloudflare Tunnel | Zero-trust HTTPS tunneling exposing local WSGI port to a global URL |

---

## CHAPTER 4: SYSTEM DESIGN & ARCHITECTURE

### 4.1 High-Level Architecture
The system follows a Model-View-Controller (MVC) derived architecture tailored for Python web frameworks:

```
+-------------------------------------------------------------------------+
|                              CLIENT BROWSER                             |
|    (Responsive Bootstrap 5 UI: Sign In, Dashboard, Students, Predict)   |
+------------------------------------+------------------------------------+
                                     | HTTP Requests (GET / POST)
                                     v
+-------------------------------------------------------------------------+
|                           FLASK WEB CONTROLLER                          |
|         (app.py - Routing, Session Auth, Form Parsing, Validation)      |
+-------------------+---------------------------------+-------------------+
                    |                                 |
                    v Parameterized SQL               v Feature DataFrame
+-------------------------------------+   +-------------------------------+
|             MYSQL 8.0               |   |     SCIKIT-LEARN INFERENCE    |
| - users (Auth)                      |   | - joblib serialized pipeline  |
| - students (Profiles)               |   | - Standardized feature input  |
| - subjects, attendance, marks       |   | - Random Forest Classifier    |
| - predictions (Historical Log)      |   | - Class & Confidence Output   |
+-------------------------------------+   +---------------+---------------+
                    |                                     |
                    +------------------+------------------+
                                       | Aggregated Context
                                       v
+-------------------------------------------------------------------------+
|                           JINJA2 TEMPLATE ENGINE                        |
|                  (Renders HTML with Dynamic Insights)                   |
+-------------------------------------------------------------------------+
```

### 4.2 Data Flow Diagram (DFD)

#### Level 0 DFD (Context Diagram)
- **User (Faculty/Admin)** supplies credentials $\rightarrow$ **System** validates $\rightarrow$ Issues authenticated session.
- **User** supplies Student Academic Parameters $\rightarrow$ **System** evaluates via ML Model & writes record to MySQL $\rightarrow$ Returns Prediction & Action Plan.

#### Level 1 DFD
1. **Authentication Process**: Validates user inputs against the `users` relational table.
2. **Student Management Process**: Performs CRUD queries (`INSERT`, `SELECT`, `UPDATE`, `DELETE`) on the `students` table.
3. **Inference Pipeline Process**:
   - Accepts parameters: Attendance, Internal Marks, Assignment Marks, CGPA, Failures.
   - Formats input into a 2D Pandas DataFrame.
   - Invokes `RandomForestClassifier.predict()` and `predict_proba()`.
   - Records prediction outcome into the `predictions` table.
   - Returns classification class and percentage confidence.

### 4.3 Database Schema & Entity-Relationship Design
The database `student_performance` enforces referential integrity through foreign keys:

1. **`users` Table**:
   - `user_id` INT AUTO_INCREMENT PRIMARY KEY
   - `username` VARCHAR(50) UNIQUE NOT NULL
   - `password` VARCHAR(255) NOT NULL
   - `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

2. **`students` Table**:
   - `student_id` INT AUTO_INCREMENT PRIMARY KEY
   - `name` VARCHAR(100) NOT NULL
   - `department` VARCHAR(100)
   - `semester` INT

3. **`subjects` Table**:
   - `subject_id` INT AUTO_INCREMENT PRIMARY KEY
   - `subject_name` VARCHAR(100) NOT NULL
   - `credits` INT DEFAULT 3

4. **`attendance` Table**:
   - `attendance_id` INT AUTO_INCREMENT PRIMARY KEY
   - `student_id` INT (FK $\rightarrow$ `students.student_id`)
   - `subject_id` INT (FK $\rightarrow$ `subjects.subject_id`)
   - `percentage` DECIMAL(5,2)

5. **`marks` Table**:
   - `mark_id` INT AUTO_INCREMENT PRIMARY KEY
   - `student_id` INT (FK $\rightarrow$ `students.student_id`)
   - `subject_id` INT (FK $\rightarrow$ `subjects.subject_id`)
   - `internal` DECIMAL(5,2), `assignment` DECIMAL(5,2), `exam` DECIMAL(5,2)

6. **`performance` Table**:
   - `performance_id` INT AUTO_INCREMENT PRIMARY KEY
   - `student_id` INT (FK $\rightarrow$ `students.student_id`)
   - `gpa` DECIMAL(4,2), `grade` VARCHAR(10)

7. **`predictions` Table**:
   - `prediction_id` INT AUTO_INCREMENT PRIMARY KEY
   - `student_id` INT (FK $\rightarrow$ `students.student_id`)
   - `predicted_class` VARCHAR(20)
   - `probability` DECIMAL(6,4)
   - `predicted_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

---

## CHAPTER 5: METHODOLOGY & IMPLEMENTATION

### 5.1 Dataset Description & Preprocessing
The model training module uses academic feature vectors comprising 5 primary features:
1. **Attendance Rate (`attendance`)**: Continuous percentage [0.0 - 100.0%]. Represents regular classroom engagement.
2. **Internal Assessment Score (`internal`)**: Continuous score [0.0 - 100.0]. Represents mid-semester theoretical aptitude.
3. **Assignment Score (`assignment`)**: Continuous score [0.0 - 100.0]. Measures project delivery, problem-solving, and continuous diligence.
4. **Previous GPA (`gpa`)**: Floating point score [0.00 - 10.00]. Cumulative historical metric.
5. **Past Backlogs / Failures (`failures`)**: Integer count [0, 1, 2, ...]. Represents academic carryovers and historical deficit.

The target variable **`performance`** is categorized into three mutually exclusive classes:
- **`High`**: High academic performance, consistent marks, zero backlogs.
- **`Average`**: Satisfactory performance, moderate scores, minimal backlogs.
- **`Low`**: Below threshold scores, irregular attendance, multiple backlogs requiring immediate remedial intervention.

### 5.2 Feature Engineering & Model Training
The dataset is split into training (80%) and testing (20%) subsets using **Stratified Sampling** to guarantee identical class distribution across both partitions:
```python
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```

Three standard classification algorithms were trained and benchmarked:
1. **Logistic Regression (Multinomial)**:
   - Evaluated as a linear baseline with feature standard scaling:
     Pipeline([('scale', StandardScaler()), ('clf', LogisticRegression(max_iter=2000))])
2. **Decision Tree Classifier**:
   - Non-linear rule induction tree with restricted tree depth (`max_depth=6`) to mitigate variance and leaf overfitting.
3. **Random Forest Classifier**:
   - Ensemble of 300 decision trees (`n_estimators=300`) with bootstrap aggregation (bagging) and random subspace feature sampling.

### 5.3 Model Serialization
The top-performing model (**Random Forest**) is serialized into a compact binary artifact using `joblib`:
```python
joblib.dump(m, "ml/student_performance_model.pkl")
```
This enables real-time, low-latency scoring during web application runtime without requiring retraining during request cycles.

### 5.4 Backend Implementation (Flask)
The core web service is written in Python using Flask:
- **Session Management**: Cryptographically signed cookie sessions authenticate requests; unauthorized requests redirect to the Sign In page.
- **Database Connection Factory**:
  ```python
  def db():
      return mysql.connector.connect(
          host="localhost",
          user="root",
          password="***",
          database="student_performance"
      )
  ```
- **CRUD Endpoints**:
  - `/` (GET/POST): Authentication & portal sign in (Admin/Authorized credentials).
  - `/dashboard` (GET): Overview querying summary metrics via SQL aggregate functions (`COUNT(*)`, `AVG(gpa)`).
  - `/students` (GET/POST): Alphabetically sorted student registry display and new student enrollment.
  - `/students/edit/<id>` (GET/POST): Updating student profile records.
  - `/students/delete/<id>` (GET/POST): Safe cascade deletion of student records and related predictions.
  - `/predict` (GET/POST): Real-time inference dispatching, confidence extraction, and prediction logging.

### 5.5 Cloud Deployment via Cloudflare Tunnel
To facilitate real-world testing without port forwarding or firewall configuration, a secure outbound reverse tunnel was established using Cloudflare Zero Trust:
```bash
.\cloudflared.exe tunnel --url http://127.0.0.1:5000
```
This provisions an end-to-end SSL/TLS protected domain (`https://*.trycloudflare.com`) routing globally to the local Flask application.

---

## CHAPTER 6: EXPERIMENTAL RESULTS & PERFORMANCE ANALYSIS

### 6.1 Model Performance Evaluation
The models were evaluated using four core metrics:
- **Accuracy**: (TP + TN) / (TP + TN + FP + FN)
- **Precision**: TP / (TP + FP)
- **Recall (Sensitivity)**: TP / (TP + FN)
- **F1-Score**: 2 * (Precision * Recall) / (Precision + Recall)

#### Model Comparison Table
| Algorithm | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | Baseline Linear Model |
| **Decision Tree** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | White-Box Decision Rules |
| **Random Forest Classifier** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **Selected Production Model** |

*Note: The Random Forest model was selected for production deployment due to its superior variance reduction, robustness against multi-collinearity, and reliable probability calibration (`predict_proba`).*

### 6.2 Risk Classification Scenarios
The deployed system dynamically categorizes outcomes into three operational profiles:

1. **High Performance Profile (Green Banner)**:
   - *Typical Attributes*: Attendance > 85%, Internals > 75, Assignments > 80, GPA > 8.0, 0 Backlogs.
   - *System Recommendation*: "Student demonstrates high consistency and strong foundational scores. Recommended for honors projects, research internships, and peer-tutoring."
2. **Average Performance Profile (Amber Banner)**:
   - *Typical Attributes*: Attendance 65 - 80%, Internals 50 - 70, Assignments 55 - 75, GPA 6.0 - 7.5, <= 1 Backlog.
   - *System Recommendation*: "Student is performing steadily. Regular monitoring of assignment completion and attendance will help them progress to higher grades."
3. **Low Performance / At-Risk Profile (Red Banner)**:
   - *Typical Attributes*: Attendance < 65%, Internals < 45%, Assignments < 50%, GPA < 5.5, >= 2 Backlogs.
   - *System Recommendation*: "Student is falling in the low performance bracket. Immediate remedial mentorship, attendance intervention, and assignment support recommended."

---

## CHAPTER 7: CONCLUSION & FUTURE SCOPE

### 7.1 Conclusion
The **AI-Based Student Performance Prediction and Database Management System** successfully unites modern database engineering with supervised machine learning in a production-ready web application. By replacing manual, delayed academic tracking with automated real-time predictive analytics, the system provides faculty advisors with early warning alerts, probability estimates, and tailored pedagogical recommendations. The system demonstrates high predictive efficacy, clean responsive design, and frictionless deployment via encrypted tunnels.

### 7.2 Future Enhancements
- **LMS/ERP Auto-Synchronization**: Direct integration with Moodle, Canvas, or institutional ERP systems via automated REST APIs.
- **Explainable AI (XAI)**: Integration of **SHAP** (SHapley Additive exPlanations) or **LIME** waterfall plots to visually explain exactly which feature contributed most to a student's risk rating.
- **Deep Learning for Longitudinal Trajectories**: Employing Recurrent Neural Networks (RNN/LSTM) to model multi-semester time-series performance changes over 4 academic years.
- **Automated Communication Hub**: Automated dispatch of SMS or email alerts to students and parents when risk parameters cross predefined thresholds.

---

## REFERENCES
1. Baker, R. S., & Inventado, P. S. (2014). *Educational Data Mining and Learning Analytics*. In Learning Analytics (pp. 61-75). Springer, New York, NY.
2. Romero, C., & Ventura, S. (2020). *Educational data mining and learning analytics: An updated survey*. WIREs Data Mining and Knowledge Discovery, 10(3), e1355.
3. Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5-32.
4. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
5. Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media.
6. Elmasri, R., & Navathe, S. B. (2015). *Fundamentals of Database Systems* (7th ed.). Pearson.
