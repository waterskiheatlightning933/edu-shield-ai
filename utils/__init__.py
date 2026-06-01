"""
EduShield AI Lite Utilities Module
Contains all helper functions for prediction, recommendations, database, and reporting
"""

from .predictor import (
    load_model,
    calculate_rule_based_score,
    determine_risk_level,
    predict_student_risk,
    get_risk_factors
)

from .recommendations import (
    get_recommendations,
    format_recommendations_for_display,
    get_action_plan,
    get_motivational_message
)

from .database import (
    init_database,
    save_student_record,
    get_all_records,
    get_student_record,
    delete_student_record,
    get_risk_distribution,
    get_high_risk_students
)

from .report_generator import (
    generate_pdf_report,
    generate_report_filename
)

__all__ = [
    # Predictor
    'load_model',
    'calculate_rule_based_score',
    'determine_risk_level',
    'predict_student_risk',
    'get_risk_factors',
    
    # Recommendations
    'get_recommendations',
    'format_recommendations_for_display',
    'get_action_plan',
    'get_motivational_message',
    
    # Database
    'init_database',
    'save_student_record',
    'get_all_records',
    'get_student_record',
    'delete_student_record',
    'get_risk_distribution',
    'get_high_risk_students',
    
    # Report Generator
    'generate_pdf_report',
    'generate_report_filename',
]
