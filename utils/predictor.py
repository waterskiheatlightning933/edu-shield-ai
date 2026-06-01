"""
Predictor module for ML model inference
Includes both ML prediction and rule-based scoring
"""

import joblib
import os
from pathlib import Path
import numpy as np

MODEL_PATH = "model/student_risk_model.pkl"

def load_model():
    """
    Load the trained machine learning model
    
    Returns:
        model: Loaded ML model, or None if model not found
    """
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            return model
        else:
            print(f"Model not found at {MODEL_PATH}")
            return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def calculate_rule_based_score(student_data):
    """
    Calculate risk score based on manual rules
    
    Args:
        student_data: Dictionary with student information
    
    Returns:
        float: Risk score from 0 to 100
    """
    risk_score = 0
    
    # Attendance rule: < 60% adds 30 points
    if student_data.get('attendance_percent', 0) < 60:
        risk_score += 30
    elif student_data.get('attendance_percent', 0) < 75:
        risk_score += 15
    
    # Quiz average rule: < 50 adds 20 points
    if student_data.get('quiz_average', 0) < 50:
        risk_score += 20
    elif student_data.get('quiz_average', 0) < 65:
        risk_score += 10
    
    # Assignment average rule: < 50 adds 15 points
    if student_data.get('assignment_average', 0) < 50:
        risk_score += 15
    elif student_data.get('assignment_average', 0) < 65:
        risk_score += 8
    
    # Study hours rule: < 2 adds 15 points
    if student_data.get('study_hours_per_day', 0) < 2:
        risk_score += 15
    elif student_data.get('study_hours_per_day', 0) < 3:
        risk_score += 8
    
    # Previous GPA rule: < 2.5 adds 20 points
    if student_data.get('previous_gpa', 0) < 2.5:
        risk_score += 20
    elif student_data.get('previous_gpa', 0) < 3.0:
        risk_score += 10
    
    # Sleep hours: < 6 adds 5 points
    if student_data.get('sleep_hours', 0) < 6:
        risk_score += 5
    
    # Internet usage: > 6 hours adds 5 points
    if student_data.get('internet_usage_hours', 0) > 6:
        risk_score += 5
    
    # Class participation: < 50% adds 5 points
    if student_data.get('class_participation', 0) < 50:
        risk_score += 5
    
    # Cap score at 100
    return min(risk_score, 100)

def determine_risk_level(risk_score):
    """
    Determine risk level based on score
    
    Args:
        risk_score: Score from 0 to 100
    
    Returns:
        str: Risk level (Low Risk, Medium Risk, High Risk)
    """
    if risk_score < 30:
        return "Low Risk"
    elif risk_score < 60:
        return "Medium Risk"
    else:
        return "High Risk"

def predict_student_risk(student_data, use_ml_model=True):
    """
    Predict student risk level using combined approach
    
    Args:
        student_data: Dictionary with student information
        use_ml_model: Whether to use ML model (True) or just rule-based (False)
    
    Returns:
        dict: Prediction result with risk level, scores, and analysis
    """
    # Calculate rule-based score
    rule_based_score = calculate_rule_based_score(student_data)
    rule_based_level = determine_risk_level(rule_based_score)
    
    result = {
        'rule_based_score': rule_based_score,
        'rule_based_level': rule_based_level,
        'ml_score': None,
        'ml_level': None,
        'final_score': rule_based_score,
        'final_level': rule_based_level,
        'model_available': False
    }
    
    # Try to use ML model if available
    if use_ml_model:
        model = load_model()
        if model:
            try:
                # Prepare features in the correct order
                features = np.array([[
                    student_data.get('attendance_percent', 0),
                    student_data.get('quiz_average', 0),
                    student_data.get('assignment_average', 0),
                    student_data.get('midterm_marks', 0),
                    student_data.get('study_hours_per_day', 0),
                    student_data.get('sleep_hours', 0),
                    student_data.get('internet_usage_hours', 0),
                    student_data.get('previous_gpa', 0),
                    student_data.get('class_participation', 0)
                ]])
                
                # Get ML prediction
                ml_prediction = model.predict(features)[0]
                ml_probability = model.predict_proba(features)[0]
                ml_score = max(ml_probability) * 100
                
                result['ml_level'] = ml_prediction
                result['ml_score'] = ml_score
                result['model_available'] = True
                
                # Average both scores for final decision
                result['final_score'] = (rule_based_score + ml_score) / 2
                result['final_level'] = determine_risk_level(result['final_score'])
                
            except Exception as e:
                print(f"Error during ML prediction: {e}")
                # Fall back to rule-based only
    
    return result

def get_risk_factors(student_data):
    """
    Identify specific factors contributing to risk
    
    Args:
        student_data: Dictionary with student information
    
    Returns:
        list: List of risk factors identified
    """
    risk_factors = []
    
    if student_data.get('attendance_percent', 0) < 60:
        risk_factors.append(f"Low attendance ({student_data.get('attendance_percent', 0)}%)")
    
    if student_data.get('quiz_average', 0) < 50:
        risk_factors.append(f"Weak quiz performance ({student_data.get('quiz_average', 0)}/100)")
    
    if student_data.get('assignment_average', 0) < 50:
        risk_factors.append(f"Low assignment scores ({student_data.get('assignment_average', 0)}/100)")
    
    if student_data.get('midterm_marks', 0) < 40:
        risk_factors.append(f"Poor midterm marks ({student_data.get('midterm_marks', 0)}/100)")
    
    if student_data.get('study_hours_per_day', 0) < 2:
        risk_factors.append(f"Insufficient study time ({student_data.get('study_hours_per_day', 0)} hours/day)")
    
    if student_data.get('previous_gpa', 0) < 2.5:
        risk_factors.append(f"Low previous GPA ({student_data.get('previous_gpa', 0)}/4.0)")
    
    if student_data.get('sleep_hours', 0) < 6:
        risk_factors.append(f"Inadequate sleep ({student_data.get('sleep_hours', 0)} hours/day)")
    
    if student_data.get('internet_usage_hours', 0) > 6:
        risk_factors.append(f"High internet usage ({student_data.get('internet_usage_hours', 0)} hours/day)")
    
    if student_data.get('class_participation', 0) < 50:
        risk_factors.append(f"Low class participation ({student_data.get('class_participation', 0)}%)")
    
    return risk_factors if risk_factors else ["Student appears to be performing well"]
