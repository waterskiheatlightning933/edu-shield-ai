"""
Report Generator module
Creates PDF reports for student risk assessments
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from datetime import datetime
import io

def generate_pdf_report(student_data, prediction_result, risk_factors, recommendations, filename=None):
    """
    Generate a professional PDF report for student risk assessment
    
    Args:
        student_data: Dictionary with student information
        prediction_result: Dictionary with prediction results
        risk_factors: List of identified risk factors
        recommendations: Dictionary of recommendations
        filename: Output filename (optional)
    
    Returns:
        bytes: PDF content as bytes, or saves to file if filename provided
    """
    
    # Create PDF buffer or file
    if filename is None:
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    else:
        doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    risk_high_style = ParagraphStyle(
        'RiskHigh',
        parent=styles['Normal'],
        textColor=colors.red,
        fontSize=12,
        spaceAfter=6
    )
    
    risk_medium_style = ParagraphStyle(
        'RiskMedium',
        parent=styles['Normal'],
        textColor=colors.HexColor('#FF8C00'),
        fontSize=12,
        spaceAfter=6
    )
    
    risk_low_style = ParagraphStyle(
        'RiskLow',
        parent=styles['Normal'],
        textColor=colors.green,
        fontSize=12,
        spaceAfter=6
    )
    
    # Title
    elements.append(Paragraph("EduShield AI Lite", title_style))
    elements.append(Paragraph("Student Academic Risk Assessment Report", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Report date
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    elements.append(Paragraph(f"<b>Report Generated:</b> {report_date}", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Student Information Section
    elements.append(Paragraph("Student Information", heading_style))
    student_info_data = [
        ['Field', 'Details'],
        ['Student Name', student_data.get('student_name', 'N/A')],
        ['Roll Number', student_data.get('roll_number', 'N/A')],
        ['Gender', student_data.get('gender', 'N/A')],
    ]
    
    student_table = Table(student_info_data, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Risk Assessment Section
    elements.append(Paragraph("Risk Assessment", heading_style))
    
    risk_level = prediction_result.get('final_level', 'Unknown')
    risk_score = prediction_result.get('final_score', 0)
    
    # Choose appropriate style based on risk level
    if risk_level == "High Risk":
        risk_style = risk_high_style
    elif risk_level == "Medium Risk":
        risk_style = risk_medium_style
    else:
        risk_style = risk_low_style
    
    risk_text = f"<b>Predicted Risk Level:</b> {risk_level}"
    elements.append(Paragraph(risk_text, risk_style))
    
    elements.append(Paragraph(f"<b>Risk Score:</b> {risk_score:.1f}/100", styles['Normal']))
    elements.append(Spacer(1, 0.15*inch))
    
    # Score breakdown if ML model was used
    if prediction_result.get('model_available'):
        elements.append(Paragraph("<b>Score Breakdown:</b>", styles['Normal']))
        score_data = [
            ['Assessment Method', 'Score'],
            ['Rule-Based Score', f"{prediction_result.get('rule_based_score', 0):.1f}"],
            ['ML Model Score', f"{prediction_result.get('ml_score', 0):.1f}"],
            ['Final Score (Average)', f"{risk_score:.1f}"]
        ]
        score_table = Table(score_data, colWidths=[3*inch, 3*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(score_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Risk Factors Section
    if risk_factors:
        elements.append(Paragraph("Identified Risk Factors", heading_style))
        for factor in risk_factors:
            elements.append(Paragraph(f"• {factor}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
    
    # Academic Performance Section
    elements.append(Paragraph("Academic Performance", heading_style))
    perf_data = [
        ['Metric', 'Value', 'Status'],
        ['Attendance', f"{student_data.get('attendance_percent', 0):.1f}%", 
         '✓ Good' if student_data.get('attendance_percent', 0) >= 75 else '✗ Needs Improvement'],
        ['Quiz Average', f"{student_data.get('quiz_average', 0):.1f}/100",
         '✓ Good' if student_data.get('quiz_average', 0) >= 70 else '✗ Needs Improvement'],
        ['Assignment Average', f"{student_data.get('assignment_average', 0):.1f}/100",
         '✓ Good' if student_data.get('assignment_average', 0) >= 70 else '✗ Needs Improvement'],
        ['Midterm Marks', f"{student_data.get('midterm_marks', 0):.1f}/100",
         '✓ Good' if student_data.get('midterm_marks', 0) >= 60 else '✗ Needs Improvement'],
        ['Previous GPA', f"{student_data.get('previous_gpa', 0):.2f}/4.0",
         '✓ Good' if student_data.get('previous_gpa', 0) >= 3.0 else '✗ Needs Improvement'],
    ]
    
    perf_table = Table(perf_data, colWidths=[2.2*inch, 2.2*inch, 1.6*inch])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(perf_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Recommendations Section
    elements.append(Paragraph("Recommendations for Improvement", heading_style))
    
    for category, recs in recommendations.items():
        if recs and category != 'general':
            category_name = category.replace('_', ' ').title()
            elements.append(Paragraph(f"<b>{category_name}:</b>", styles['Normal']))
            for rec in recs:
                elements.append(Paragraph(f"• {rec}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # General recommendations/motivation
    if recommendations.get('general'):
        elements.append(Paragraph("<b>Motivational Note:</b>", styles['Normal']))
        for rec in recommendations['general']:
            elements.append(Paragraph(f"• {rec}", styles['Normal']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    elements.append(Spacer(1, 0.2*inch))
    footer_text = "This report is generated by EduShield AI Lite - Student Academic Risk Assessment System. " \
                  "Please consult with your academic advisor for personalized guidance."
    elements.append(Paragraph(footer_text, ParagraphStyle('footer', parent=styles['Normal'], 
                                                           fontSize=9, textColor=colors.grey)))
    
    # Build PDF
    doc.build(elements)
    
    # Return bytes if buffer was used
    if filename is None:
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    else:
        return True

def generate_report_filename(student_name, roll_number):
    """
    Generate standardized report filename
    
    Args:
        student_name: Student name
        roll_number: Student roll number
    
    Returns:
        str: Filename
    """
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"report_{roll_number}_{date_str}.pdf"
