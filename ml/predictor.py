import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "student_performance_model.pkl")

# Cached model instance
_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        if os.path.exists(MODEL_PATH):
            _MODEL = joblib.load(MODEL_PATH)
        else:
            raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
    return _MODEL

def predict_student_performance(attendance, internal, assignment, gpa, failures, lab_marks=0, project_marks=0):
    """
    Computes Random Forest inference, continuous Predicted GPA,
    4-tier performance category (Excellent/Good/Average/At Risk),
    confidence score, automated risk detection, and personalized recommendations.
    """
    model = get_model()

    # Factored internal marks if lab/project specified
    exam_val = float(internal)
    lab_val = float(lab_marks or 0)
    proj_val = float(project_marks or 0)
    if lab_val > 0 or proj_val > 0:
        internal_val = round((exam_val * 0.6) + (lab_val * 0.2) + (proj_val * 0.2), 2)
    else:
        internal_val = exam_val

    att_val = float(attendance)
    assign_val = float(assignment)
    gpa_val = float(gpa)
    fail_val = float(failures)

    features = [att_val, internal_val, assign_val, gpa_val, fail_val]
    feature_df = pd.DataFrame([features], columns=["attendance", "internal", "assignment", "gpa", "failures"])

    # Model inference
    pred_class = model.predict(feature_df)[0]
    probabilities = model.predict_proba(feature_df)[0]
    confidence = float(np.max(probabilities))

    # Calculate Continuous Predicted GPA (scale 0.0 - 10.0)
    # Balanced academic calibration
    base_calc = (
        (internal_val * 0.35) +
        (assign_val * 0.25) +
        (att_val * 0.15) +
        (gpa_val * 10.0 * 0.25) -
        (fail_val * 4.5)
    )
    predicted_gpa = round(max(1.0, min(10.0, base_calc / 10.0)), 2)

    # 4-Tier Performance Categorization
    if predicted_gpa >= 8.5 or (pred_class == "High" and predicted_gpa >= 8.0 and fail_val == 0):
        category = "Excellent"
        badge_class = "success"
        color = "#10b981"
    elif predicted_gpa >= 7.0 or (pred_class == "High"):
        category = "Good"
        badge_class = "info"
        color = "#38bdf8"
    elif predicted_gpa >= 5.5 or (pred_class == "Average"):
        category = "Average"
        badge_class = "warning"
        color = "#f59e0b"
    else:
        category = "At Risk"
        badge_class = "danger"
        color = "#ef4444"

    # Risk detection
    risks = detect_academic_risks(att_val, internal_val, assign_val, gpa_val, fail_val, predicted_gpa)

    # Personalized recommendations
    recommendations = generate_personalized_recommendations(risks, att_val, internal_val, assign_val, fail_val)

    return {
        "pred_class": pred_class,
        "category": category,
        "predicted_gpa": predicted_gpa,
        "confidence": round(confidence * 100, 1),
        "model_name": "Random Forest Classifier (Ensemble)",
        "risks": risks,
        "recommendations": recommendations,
        "badge_class": badge_class,
        "color": color,
        "internal_val": internal_val
    }

def detect_academic_risks(attendance, internal, assignment, gpa, failures, predicted_gpa):
    """
    Automatically identifies academic vulnerabilities:
    - Low attendance (<75%)
    - Internal exam weakness (<60)
    - Assignment shortage (<65)
    - Active backlogs/failures (>0)
    - Critical At-Risk Student alert
    """
    risks = []
    if attendance < 75.0:
        risks.append({
            "type": "attendance",
            "severity": "high" if attendance < 65.0 else "medium",
            "icon": "bi-person-x-fill",
            "title": "Low Attendance Alert",
            "message": f"Attendance is at {attendance:.1f}% (below institutional 75% threshold). Risk of semester exam debarment."
        })
    if internal < 60.0:
        risks.append({
            "type": "internal",
            "severity": "high" if internal < 50.0 else "medium",
            "icon": "bi-clipboard2-x-fill",
            "title": "Internal Exam Weakness",
            "message": f"Continuous internal score is {internal:.1f}/100. Conceptual gaps in core curriculum."
        })
    if assignment < 65.0:
        risks.append({
            "type": "assignment",
            "severity": "medium",
            "icon": "bi-journal-x",
            "title": "Assignment Shortage",
            "message": f"Assignment score is {assignment:.1f}/100. Pending submissions and incomplete lab records."
        })
    if failures > 0:
        risks.append({
            "type": "backlogs",
            "severity": "high",
            "icon": "bi-exclamation-triangle-fill",
            "title": "Active Backlogs / Failures",
            "message": f"{int(failures)} active backlog/failed course(s) requiring remediation."
        })
    if predicted_gpa < 5.8 or len(risks) >= 2 or failures > 0:
        risks.append({
            "type": "at_risk_student",
            "severity": "critical",
            "icon": "bi-shield-exclamation",
            "title": "🚨 At-Risk Student Classification",
            "message": "Student trajectory triggers high academic concern. Priority mentoring & intervention recommended."
        })
    return risks

def generate_personalized_recommendations(risks, attendance, internal, assignment, failures):
    """
    Generates actionable, student-specific recommendations based on detected risks.
    """
    recs = []
    if attendance < 75.0:
        recs.append({
            "icon": "bi-calendar-check-fill",
            "color": "#38bdf8",
            "title": "Increase Attendance Above 85%",
            "detail": f"Currently at {attendance:.1f}%. Attending remaining lectures and lab sessions regularly will recover eligibility and continuous marks."
        })
    if internal < 60.0:
        recs.append({
            "icon": "bi-book-half",
            "color": "#c084fc",
            "title": "Focus on Core Fundamentals & Mathematics",
            "detail": "Dedicate revision time to foundational concepts, Data Structures, and problem-solving modules with faculty mentoring."
        })
    if assignment < 65.0:
        recs.append({
            "icon": "bi-check2-circle",
            "color": "#fbbf24",
            "title": "Complete Pending Assignments & Lab Worksheets",
            "detail": f"Boost continuous evaluation score (current {assignment:.1f}/100) by submitting all pending case studies and reports."
        })
    if failures > 0:
        recs.append({
            "icon": "bi-mortarboard-fill",
            "color": "#f87171",
            "title": "Enroll in Remedial Coaching Sessions",
            "detail": f"Clear {int(failures)} pending backlog(s) by participating in faculty remedial clinics and peer study groups."
        })
    if not recs:
        recs.append({
            "icon": "bi-stars",
            "color": "#10b981",
            "title": "Maintain High Academic Consistency",
            "detail": "Exemplary performance across all modules. Recommended for honors projects, research internships, and peer tutoring."
        })
    return recs

def simulate_what_if(current_metrics, improved_metrics):
    """
    What-If Simulation Engine:
    Compares baseline student parameters against improved target parameters:
    Attendance: 70% -> 90%
    Assignment: 60 -> 85
    Internal: 65 -> 80
    Returns current GPA, improved GPA, expected delta improvement, and category transition.
    """
    current_res = predict_student_performance(
        attendance=current_metrics.get("attendance", 75),
        internal=current_metrics.get("internal", 65),
        assignment=current_metrics.get("assignment", 65),
        gpa=current_metrics.get("gpa", 6.5),
        failures=current_metrics.get("failures", 0),
        lab_marks=current_metrics.get("lab_marks", 0),
        project_marks=current_metrics.get("project_marks", 0)
    )

    improved_res = predict_student_performance(
        attendance=improved_metrics.get("attendance", 85),
        internal=improved_metrics.get("internal", 80),
        assignment=improved_metrics.get("assignment", 80),
        gpa=improved_metrics.get("gpa", 6.5),
        failures=improved_metrics.get("failures", 0),
        lab_marks=improved_metrics.get("lab_marks", 0),
        project_marks=improved_metrics.get("project_marks", 0)
    )

    current_gpa = current_res["predicted_gpa"]
    improved_gpa = improved_res["predicted_gpa"]
    delta = round(improved_gpa - current_gpa, 2)
    delta_str = f"+{delta:.2f}" if delta > 0 else f"{delta:.2f}"

    return {
        "current_gpa": current_gpa,
        "current_category": current_res["category"],
        "current_confidence": current_res["confidence"],
        "current_badge": current_res["badge_class"],
        "improved_gpa": improved_gpa,
        "improved_category": improved_res["category"],
        "improved_confidence": improved_res["confidence"],
        "improved_badge": improved_res["badge_class"],
        "expected_improvement": delta_str,
        "delta_val": delta,
        "transition_text": f"{current_res['category']} -> {improved_res['category']}"
    }
