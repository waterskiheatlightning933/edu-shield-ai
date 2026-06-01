"""
Recommendations module
Provides personalized recommendations based on student risk factors
"""

def get_recommendations(student_data, risk_factors):
    """
    Generate personalized recommendations based on student performance
    
    Args:
        student_data: Dictionary with student information
        risk_factors: List of identified risk factors
    
    Returns:
        dict: Categorized recommendations
    """
    recommendations = {
        'attendance': [],
        'academic': [],
        'time_management': [],
        'health': [],
        'general': []
    }
    
    # Attendance recommendations
    if student_data.get('attendance_percent', 0) < 60:
        recommendations['attendance'].extend([
            "⚠️ URGENT: Attendance is critical. Attend at least 80% of classes starting now.",
            "Meet with your class teacher to discuss attendance issues.",
            "Set daily calendar reminders for classes."
        ])
    elif student_data.get('attendance_percent', 0) < 75:
        recommendations['attendance'].append(
            "Improve attendance to 80%+ to avoid academic consequences."
        )
    
    # Quiz & Assignment recommendations
    if student_data.get('quiz_average', 0) < 50:
        recommendations['academic'].extend([
            "⚠️ Quiz performance needs improvement. Attempt practice quizzes weekly.",
            "Review previous week's quiz topics before each test.",
            "Form study group with high-performing classmates."
        ])
    elif student_data.get('quiz_average', 0) < 65:
        recommendations['academic'].append(
            "Increase quiz preparation time. Target 70%+ average."
        )
    
    if student_data.get('assignment_average', 0) < 50:
        recommendations['academic'].extend([
            "Complete assignments on time and review before submission.",
            "Ask your instructor for feedback on your assignments.",
            "Use office hours to clarify difficult concepts."
        ])
    elif student_data.get('assignment_average', 0) < 65:
        recommendations['academic'].append(
            "Dedicate more time to assignments for better understanding."
        )
    
    # Midterm recommendations
    if student_data.get('midterm_marks', 0) < 40:
        recommendations['academic'].extend([
            "Start exam preparation 4 weeks in advance.",
            "Solve previous year papers and mock tests.",
            "Focus on fundamental concepts before complex topics."
        ])
    elif student_data.get('midterm_marks', 0) < 60:
        recommendations['academic'].append(
            "Strengthen weak areas identified in midterm exam."
        )
    
    # Study time recommendations
    if student_data.get('study_hours_per_day', 0) < 2:
        recommendations['time_management'].extend([
            "⚠️ Study time is very low. Increase to at least 2.5-3 hours daily.",
            "Create a structured daily study schedule.",
            "Eliminate distractions during study sessions.",
            "Use Pomodoro technique: 25 min study + 5 min break."
        ])
    elif student_data.get('study_hours_per_day', 0) < 3:
        recommendations['time_management'].append(
            "Gradually increase daily study hours to 3+ for better retention."
        )
    
    # GPA recommendations
    if student_data.get('previous_gpa', 0) < 2.5:
        recommendations['academic'].extend([
            "Previous GPA indicates need for strong intervention.",
            "Get tutoring in subjects where you struggle.",
            "Attend all classes and maintain consistent study habits."
        ])
    elif student_data.get('previous_gpa', 0) < 3.0:
        recommendations['academic'].append(
            "Maintain consistent efforts to improve GPA towards 3.0+."
        )
    
    # Sleep recommendations
    if student_data.get('sleep_hours', 0) < 6:
        recommendations['health'].extend([
            "Sleep is critical for learning. Aim for 7-8 hours daily.",
            "Maintain consistent sleep schedule (same time daily).",
            "Avoid late-night study sessions; quality matters over quantity."
        ])
    elif student_data.get('sleep_hours', 0) < 7:
        recommendations['health'].append(
            "Try to get 7-8 hours of sleep for better cognitive performance."
        )
    
    # Internet usage recommendations
    if student_data.get('internet_usage_hours', 0) > 6:
        recommendations['time_management'].extend([
            "Reduce social media usage during study hours.",
            "Use app blockers during study sessions.",
            "Set screen time limits on your devices."
        ])
    
    # Class participation
    if student_data.get('class_participation', 0) < 50:
        recommendations['general'].extend([
            "Increase classroom participation and ask questions.",
            "Prepare notes before class to engage better.",
            "Join discussion forums or study groups."
        ])
    
    # Default general recommendations
    if not any(recommendations.values()):
        recommendations['general'].append(
            "✅ Great performance! Continue maintaining these excellent habits."
        )
    else:
        recommendations['general'].append(
            "Remember: Small consistent improvements lead to big results. You've got this! 💪"
        )
    
    return recommendations

def format_recommendations_for_display(recommendations):
    """
    Format recommendations into readable sections
    
    Args:
        recommendations: Dictionary of recommendations by category
    
    Returns:
        str: Formatted recommendations for display
    """
    formatted = ""
    
    category_titles = {
        'attendance': '📚 Attendance',
        'academic': '📖 Academic Performance',
        'time_management': '⏰ Time Management',
        'health': '💚 Health & Well-being',
        'general': '🎯 General Tips'
    }
    
    for category, title in category_titles.items():
        if recommendations.get(category):
            formatted += f"\n### {title}\n"
            for rec in recommendations[category]:
                formatted += f"- {rec}\n"
    
    return formatted

def get_action_plan(student_data, risk_level):
    """
    Generate a time-based action plan
    
    Args:
        student_data: Student information
        risk_level: Current risk level (Low/Medium/High)
    
    Returns:
        dict: Action plan with timeframes
    """
    action_plan = {}
    
    if risk_level == "High Risk":
        action_plan = {
            'immediate': [
                "Attend all classes for the next 2 weeks",
                "Complete all pending assignments",
                "Schedule meeting with academic advisor",
                "Reduce internet usage to 3 hours/day"
            ],
            'week_1_2': [
                "Attend 5+ tutoring sessions",
                "Improve daily study to 3+ hours",
                "Join study group",
                "Get feedback on assignments"
            ],
            'week_3_4': [
                "Complete weekly practice quizzes",
                "Prepare for upcoming assessments",
                "Maintain attendance streak",
                "Review progress with mentor"
            ]
        }
    
    elif risk_level == "Medium Risk":
        action_plan = {
            'immediate': [
                "Attend 90%+ classes in current semester",
                "Increase daily study to 2.5 hours",
                "Complete assignments on time"
            ],
            'week_1_2': [
                "Review weak topics",
                "Attempt 3 practice quizzes",
                "Improve GPA focus areas"
            ],
            'week_3_4': [
                "Maintain consistent habits",
                "Monitor quiz performance",
                "Check progress on GPA improvement"
            ]
        }
    
    else:  # Low Risk
        action_plan = {
            'immediate': [
                "Maintain current attendance level",
                "Continue good study habits"
            ],
            'week_1_2': [
                "Help struggling classmates",
                "Explore advanced topics",
                "Prepare for higher-level courses"
            ],
            'week_3_4': [
                "Mentor other students",
                "Maintain excellence"
            ]
        }
    
    return action_plan

def get_motivational_message(risk_level, risk_score):
    """
    Get motivational message based on risk level
    
    Args:
        risk_level: Current risk level
        risk_score: Risk score (0-100)
    
    Returns:
        str: Motivational message
    """
    messages = {
        'Low Risk': [
            "🌟 You're doing great! Keep up the excellent work!",
            "💪 Your dedication shows. Stay focused!",
            "🎉 Excellent performance! You're on the right track!"
        ],
        'Medium Risk': [
            "📈 You have potential! Small improvements will help.",
            "🎯 Stay focused on your goals. You can do better!",
            "💡 There's room for improvement. Let's work on it together!"
        ],
        'High Risk': [
            "⚠️ This is a wake-up call. You need to act now!",
            "🚀 It's time to turn things around. You've got this!",
            "🛟 Don't worry, we're here to help. Let's improve together!"
        ]
    }
    
    message = messages.get(risk_level, ["Keep up the work!"])[0]
    return message
