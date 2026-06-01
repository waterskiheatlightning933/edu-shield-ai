"""
EduShield AI Lite - Student Academic Risk Assessment
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.predictor import predict_student_risk, get_risk_factors
from utils.recommendations import (
    get_recommendations, format_recommendations_for_display, 
    get_action_plan, get_motivational_message
)
from utils.database import (
    init_database, save_student_record, get_all_records, 
    get_student_record, delete_student_record, get_risk_distribution, get_high_risk_students
)
from utils.report_generator import generate_pdf_report, generate_report_filename

# Page configuration
st.set_page_config(
    page_title="EduShield AI Lite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_database()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .risk-high {
        background-color: #ffcccc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #cc0000;
    }
    .risk-medium {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ff9800;
    }
    .risk-low {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #28a745;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("# 🛡️ EduShield AI Lite")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📝 Manual Prediction", "📊 Student Records", 
     "📈 Analytics Dashboard", "📋 PDF Report", "ℹ️ About Project"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "EduShield AI Lite helps identify at-risk students early using machine learning and rule-based analysis."
)

# ============================================================================
# PAGE 1: HOME
# ============================================================================
if page == "🏠 Home":
    st.markdown("<div class='main-header'>🛡️ EduShield AI Lite</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666;'>Student Academic Risk Prediction System</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Students", len(get_all_records()))
    
    with col2:
        high_risk = len(get_all_records()[get_all_records()['predicted_risk_level'] == 'High Risk']) if len(get_all_records()) > 0 else 0
        st.metric("High Risk Students", high_risk)
    
    with col3:
        st.metric("Database Status", "✅ Active")
    
    st.markdown("---")
    
    st.markdown("### 📌 System Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 What is EduShield AI Lite?
        
        EduShield AI Lite is an intelligent student monitoring system that:
        - **Predicts** academic risk levels for students
        - **Identifies** key risk factors affecting performance
        - **Recommends** personalized improvement strategies
        - **Tracks** student progress over time
        - **Generates** professional assessment reports
        
        #### 🚀 Key Features
        - ✅ Manual student entry form
        - ✅ ML + Rule-based predictions
        - ✅ Risk scoring (0-100)
        - ✅ Personalized recommendations
        - ✅ Student database with SQLite
        - ✅ Analytics dashboard
        - ✅ PDF report generation
        """)
    
    with col2:
        st.markdown("""
        #### 🎓 How It Works
        
        **Step 1:** Teacher enters student details manually
        
        **Step 2:** System analyzes performance metrics
        
        **Step 3:** ML model + rules generate predictions
        
        **Step 4:** Risk level and score displayed
        
        **Step 5:** Personalized recommendations provided
        
        **Step 6:** Exportable PDF report generated
        
        #### 📊 Risk Levels
        - 🟢 **Low Risk** (0-30): Student performing well
        - 🟡 **Medium Risk** (30-60): Needs attention
        - 🔴 **High Risk** (60-100): Urgent intervention needed
        """)
    
    st.markdown("---")
    
    st.markdown("### 🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Enter Student Data**
        - Go to "Manual Prediction" page
        - Fill in student details
        - Submit to get prediction
        """)
    
    with col2:
        st.markdown("""
        **2. View Analytics**
        - Go to "Analytics Dashboard"
        - See risk distribution charts
        - Monitor high-risk students
        """)
    
    st.markdown("---")
    
    st.info("👉 **Start by going to 'Manual Prediction' to enter student details and get your first prediction!**")

# ============================================================================
# PAGE 2: MANUAL PREDICTION
# ============================================================================
elif page == "📝 Manual Prediction":
    st.markdown("<div class='main-header'>📝 Manual Student Entry & Prediction</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Create form
    with st.form("student_form", clear_on_submit=False):
        st.markdown("### Student Information")
        
        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input("Student Name *", placeholder="e.g., John Doe")
            roll_number = st.text_input("Roll Number *", placeholder="e.g., CS001")
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
            class_level = st.selectbox("Class/Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        
        st.markdown("### Academic Performance")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            attendance = st.slider("Attendance %", 0, 100, 75, step=5)
            quiz_avg = st.slider("Quiz Average (/100)", 0, 100, 70, step=5)
        
        with col2:
            assignment_avg = st.slider("Assignment Average (/100)", 0, 100, 75, step=5)
            midterm = st.slider("Midterm Marks (/100)", 0, 100, 70, step=5)
        
        with col3:
            previous_gpa = st.slider("Previous GPA (/4.0)", 0.0, 4.0, 3.0, step=0.1)
            class_participation = st.slider("Class Participation %", 0, 100, 70, step=5)
        
        st.markdown("### Personal Habits")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            study_hours = st.number_input("Study Hours per Day", 0.0, 12.0, 2.5, step=0.5)
        
        with col2:
            sleep_hours = st.number_input("Sleep Hours per Day", 0.0, 12.0, 7.0, step=0.5)
        
        with col3:
            internet_hours = st.number_input("Internet Usage Hours per Day", 0.0, 24.0, 4.0, step=0.5)
        
        st.markdown("---")
        
        submit_button = st.form_submit_button("🔮 Predict Risk Level", use_container_width=True)
    
    # Process prediction
    if submit_button:
        if not student_name or not roll_number:
            st.error("❌ Please fill in Student Name and Roll Number")
        else:
            # Prepare student data
            student_data = {
                'student_name': student_name,
                'roll_number': roll_number,
                'gender': gender,
                'class_level': class_level,
                'attendance_percent': attendance,
                'quiz_average': quiz_avg,
                'assignment_average': assignment_avg,
                'midterm_marks': midterm,
                'study_hours_per_day': study_hours,
                'sleep_hours': sleep_hours,
                'internet_usage_hours': internet_hours,
                'previous_gpa': previous_gpa,
                'class_participation': class_participation,
            }
            
            # Get prediction
            with st.spinner("🔮 Analyzing student performance..."):
                prediction = predict_student_risk(student_data)
                risk_factors = get_risk_factors(student_data)
                recommendations = get_recommendations(student_data, risk_factors)
                
                # Save to database
                student_data['predicted_risk_level'] = prediction['final_level']
                student_data['risk_score'] = prediction['final_score']
                save_student_record(student_data)
            
            st.success("✅ Prediction completed and saved!")
            st.markdown("---")
            
            # Display prediction results
            st.markdown("### 🎯 Prediction Results")
            
            risk_level = prediction['final_level']
            risk_score = prediction['final_score']
            
            # Risk indicator with color
            if risk_level == "High Risk":
                st.markdown(f"<div class='risk-high'><h2>⚠️ {risk_level}</h2><p>Risk Score: {risk_score:.1f}/100</p></div>", unsafe_allow_html=True)
            elif risk_level == "Medium Risk":
                st.markdown(f"<div class='risk-medium'><h2>🟡 {risk_level}</h2><p>Risk Score: {risk_score:.1f}/100</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='risk-low'><h2>✅ {risk_level}</h2><p>Risk Score: {risk_score:.1f}/100</p></div>", unsafe_allow_html=True)
            
            # Score breakdown
            if prediction['model_available']:
                st.markdown("#### 📊 Score Breakdown")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rule-Based Score", f"{prediction['rule_based_score']:.1f}")
                with col2:
                    st.metric("ML Model Score", f"{prediction['ml_score']:.1f}")
                with col3:
                    st.metric("Final Score", f"{prediction['final_score']:.1f}")
            else:
                st.info("💡 ML model not available. Using rule-based assessment only.")
                st.metric("Risk Score", f"{prediction['final_score']:.1f}/100")
            
            st.markdown("---")
            
            # Risk factors
            if risk_factors:
                st.markdown("#### ⚠️ Identified Risk Factors")
                for factor in risk_factors:
                    st.warning(f"• {factor}")
            
            st.markdown("---")
            
            # Motivational message
            message = get_motivational_message(risk_level, risk_score)
            st.info(message)
            
            st.markdown("---")
            
            # Recommendations
            st.markdown("#### 💡 Personalized Recommendations")
            
            for category, recs in recommendations.items():
                if recs and category != 'general':
                    with st.expander(f"📌 {category.replace('_', ' ').title()}"):
                        for rec in recs:
                            st.write(f"• {rec}")
            
            # General recommendations
            if recommendations.get('general'):
                with st.expander("🎯 General Tips"):
                    for rec in recommendations['general']:
                        st.write(f"• {rec}")
            
            st.markdown("---")
            
            # Action plan
            st.markdown("#### 📅 Action Plan")
            action_plan = get_action_plan(student_data, risk_level)
            
            with st.expander("Immediate Actions (This Week)", expanded=True):
                if 'immediate' in action_plan:
                    for action in action_plan['immediate']:
                        st.write(f"✓ {action}")
            
            with st.expander("Week 1-2 Actions"):
                if 'week_1_2' in action_plan:
                    for action in action_plan['week_1_2']:
                        st.write(f"✓ {action}")
            
            with st.expander("Week 3-4 Actions"):
                if 'week_3_4' in action_plan:
                    for action in action_plan['week_3_4']:
                        st.write(f"✓ {action}")
            
            st.markdown("---")
            
            # Download PDF button
            st.markdown("#### 📥 Export Report")
            pdf_data = generate_pdf_report(student_data, prediction, risk_factors, recommendations)
            filename = generate_report_filename(student_name, roll_number)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_data,
                file_name=filename,
                mime="application/pdf"
            )

# ============================================================================
# PAGE 3: STUDENT RECORDS
# ============================================================================
elif page == "📊 Student Records":
    st.markdown("<div class='main-header'>📊 Student Records Database</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Get all records
    all_records = get_all_records()
    
    if len(all_records) == 0:
        st.info("📭 No student records found. Start by adding a student in 'Manual Prediction' page.")
    else:
        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students", len(all_records))
        with col2:
            high_risk_count = len(all_records[all_records['predicted_risk_level'] == 'High Risk'])
            st.metric("High Risk Students", high_risk_count)
        with col3:
            avg_score = all_records['risk_score'].mean()
            st.metric("Average Risk Score", f"{avg_score:.1f}")
        
        st.markdown("---")
        
        # Search and filter
        st.markdown("### 🔍 Search & Filter")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_name = st.text_input("Search by Name", "")
        
        with col2:
            search_roll = st.text_input("Search by Roll Number", "")
        
        with col3:
            filter_risk = st.multiselect(
                "Filter by Risk Level",
                ["Low Risk", "Medium Risk", "High Risk"],
                default=["Low Risk", "Medium Risk", "High Risk"]
            )
        
        # Apply filters
        filtered_records = all_records.copy()
        
        if search_name:
            filtered_records = filtered_records[
                filtered_records['student_name'].str.contains(search_name, case=False, na=False)
            ]
        
        if search_roll:
            filtered_records = filtered_records[
                filtered_records['roll_number'].str.contains(search_roll, case=False, na=False)
            ]
        
        if filter_risk:
            filtered_records = filtered_records[filtered_records['predicted_risk_level'].isin(filter_risk)]
        
        st.markdown(f"### 📋 Showing {len(filtered_records)} records")
        
        # Display records table
        display_cols = ['student_name', 'roll_number', 'gender', 'attendance_percent', 
                       'quiz_average', 'previous_gpa', 'predicted_risk_level', 'risk_score', 'created_date']
        
        if len(filtered_records) > 0:
            # Format display
            df_display = filtered_records[display_cols].copy()
            df_display.columns = ['Name', 'Roll #', 'Gender', 'Attendance %', 'Quiz Avg', 'GPA', 'Risk Level', 'Risk Score', 'Date']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            
            # Export to CSV
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"student_records_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No records match your search criteria.")
        
        st.markdown("---")
        
        # Individual record management
        st.markdown("### ⚙️ Manage Individual Records")
        
        if len(all_records) > 0:
            selected_roll = st.selectbox(
                "Select Student",
                all_records['roll_number'].tolist(),
                format_func=lambda x: f"{x} - {all_records[all_records['roll_number']==x]['student_name'].values[0]}"
            )
            
            if selected_roll:
                record = get_student_record(selected_roll)
                
                if record:
                    st.markdown(f"#### {record.get('student_name', 'Unknown')}")
                    
                    # Display record details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Risk Level", record.get('predicted_risk_level', 'N/A'))
                        st.metric("Risk Score", f"{record.get('risk_score', 0):.1f}")
                        st.metric("Attendance", f"{record.get('attendance_percent', 0):.1f}%")
                    
                    with col2:
                        st.metric("Quiz Average", f"{record.get('quiz_average', 0):.1f}")
                        st.metric("Previous GPA", f"{record.get('previous_gpa', 0):.2f}")
                        st.metric("Study Hours/Day", f"{record.get('study_hours_per_day', 0):.1f}")
                    
                    st.markdown("---")
                    
                    # Delete option
                    if st.button(f"🗑️ Delete {selected_roll}", key="delete_btn"):
                        if delete_student_record(selected_roll):
                            st.success("✅ Record deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Error deleting record.")

# ============================================================================
# PAGE 4: ANALYTICS DASHBOARD
# ============================================================================
elif page == "📈 Analytics Dashboard":
    st.markdown("<div class='main-header'>📈 Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    all_records = get_all_records()
    
    if len(all_records) == 0:
        st.info("📭 No data available yet. Add student records to see analytics.")
    else:
        # Key metrics
        st.markdown("### 📊 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", len(all_records))
        
        with col2:
            avg_attendance = all_records['attendance_percent'].mean()
            st.metric("Avg Attendance", f"{avg_attendance:.1f}%")
        
        with col3:
            avg_gpa = all_records['previous_gpa'].mean()
            st.metric("Avg GPA", f"{avg_gpa:.2f}")
        
        with col4:
            avg_risk = all_records['risk_score'].mean()
            st.metric("Avg Risk Score", f"{avg_risk:.1f}")
        
        st.markdown("---")
        
        # Charts
        st.markdown("### 📉 Charts & Visualizations")
        
        col1, col2 = st.columns(2)
        
        # Risk Distribution Pie Chart
        with col1:
            risk_dist = get_risk_distribution()
            if not risk_dist.empty:
                fig_pie = px.pie(
                    risk_dist,
                    values='count',
                    names='predicted_risk_level',
                    title="Risk Level Distribution",
                    color_discrete_map={
                        'Low Risk': '#28a745',
                        'Medium Risk': '#ff9800',
                        'High Risk': '#cc0000'
                    }
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.warning("No data available for risk distribution")
        
        # Attendance vs Risk
        with col2:
            fig_scatter = px.scatter(
                all_records,
                x='attendance_percent',
                y='risk_score',
                color='predicted_risk_level',
                title="Attendance vs Risk Score",
                labels={'attendance_percent': 'Attendance %', 'risk_score': 'Risk Score'},
                color_discrete_map={
                    'Low Risk': '#28a745',
                    'Medium Risk': '#ff9800',
                    'High Risk': '#cc0000'
                }
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        # GPA Distribution
        with col1:
            fig_gpa = px.histogram(
                all_records,
                x='previous_gpa',
                nbins=10,
                title="GPA Distribution",
                labels={'previous_gpa': 'GPA', 'count': 'Number of Students'},
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig_gpa, use_container_width=True)
        
        # Quiz Average Distribution
        with col2:
            fig_quiz = px.histogram(
                all_records,
                x='quiz_average',
                nbins=10,
                title="Quiz Average Distribution",
                labels={'quiz_average': 'Quiz Average', 'count': 'Number of Students'},
                color_discrete_sequence=['#ff7f0e']
            )
            st.plotly_chart(fig_quiz, use_container_width=True)
        
        st.markdown("---")
        
        # High-risk students
        st.markdown("### 🚨 Top High-Risk Students")
        high_risk = get_high_risk_students()
        
        if not high_risk.empty:
            st.dataframe(
                high_risk,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ No high-risk students! Great work!")
        
        st.markdown("---")
        
        # Attendance Distribution
        st.markdown("### 📊 Additional Metrics")
        
        fig_box = px.box(
            all_records,
            y='attendance_percent',
            x='predicted_risk_level',
            title="Attendance by Risk Level",
            labels={'attendance_percent': 'Attendance %', 'predicted_risk_level': 'Risk Level'},
            color='predicted_risk_level',
            color_discrete_map={
                'Low Risk': '#28a745',
                'Medium Risk': '#ff9800',
                'High Risk': '#cc0000'
            }
        )
        st.plotly_chart(fig_box, use_container_width=True)

# ============================================================================
# PAGE 5: PDF REPORT
# ============================================================================
elif page == "📋 PDF Report":
    st.markdown("<div class='main-header'>📋 Generate PDF Report</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    all_records = get_all_records()
    
    if len(all_records) == 0:
        st.info("📭 No student records found. Please add students first.")
    else:
        st.markdown("### Select Student for Report")
        
        selected_roll = st.selectbox(
            "Choose Student",
            all_records['roll_number'].tolist(),
            format_func=lambda x: f"{x} - {all_records[all_records['roll_number']==x]['student_name'].values[0]}"
        )
        
        if selected_roll:
            record = get_student_record(selected_roll)
            
            if record:
                # Display student info
                st.markdown(f"### 📊 {record.get('student_name', 'Unknown')}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Roll Number", record.get('roll_number', 'N/A'))
                    st.metric("Risk Level", record.get('predicted_risk_level', 'N/A'))
                
                with col2:
                    st.metric("Risk Score", f"{record.get('risk_score', 0):.1f}/100")
                    st.metric("Attendance", f"{record.get('attendance_percent', 0):.1f}%")
                
                with col3:
                    st.metric("Quiz Average", f"{record.get('quiz_average', 0):.1f}")
                    st.metric("Previous GPA", f"{record.get('previous_gpa', 0):.2f}")
                
                st.markdown("---")
                
                # Prepare data for report generation
                student_data = {
                    'student_name': record.get('student_name', 'N/A'),
                    'roll_number': record.get('roll_number', 'N/A'),
                    'gender': record.get('gender', 'N/A'),
                    'attendance_percent': record.get('attendance_percent', 0),
                    'quiz_average': record.get('quiz_average', 0),
                    'assignment_average': record.get('assignment_average', 0),
                    'midterm_marks': record.get('midterm_marks', 0),
                    'study_hours_per_day': record.get('study_hours_per_day', 0),
                    'sleep_hours': record.get('sleep_hours', 0),
                    'internet_usage_hours': record.get('internet_usage_hours', 0),
                    'previous_gpa': record.get('previous_gpa', 0),
                    'class_participation': record.get('class_participation', 0),
                }
                
                # Get prediction details
                prediction = predict_student_risk(student_data)
                risk_factors = get_risk_factors(student_data)
                recommendations = get_recommendations(student_data, risk_factors)
                
                st.markdown("### 📄 Generate Report")
                
                if st.button("🔄 Generate PDF Report", use_container_width=True):
                    with st.spinner("📄 Generating PDF..."):
                        pdf_data = generate_pdf_report(student_data, prediction, risk_factors, recommendations)
                        filename = generate_report_filename(
                            student_data['student_name'],
                            student_data['roll_number']
                        )
                    
                    st.success("✅ PDF generated successfully!")
                    
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )

# ============================================================================
# PAGE 6: ABOUT PROJECT
# ============================================================================
elif page == "ℹ️ About Project":
    st.markdown("<div class='main-header'>ℹ️ About EduShield AI Lite</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    ## 🎓 Project Overview
    
    **EduShield AI Lite** is a comprehensive student academic risk assessment and early intervention system. 
    It combines machine learning and rule-based analysis to identify students at risk of academic failure, 
    enabling timely intervention by educators and support staff.
    
    ---
    
    ## 🎯 Project Objectives
    
    1. **Early Detection**: Identify at-risk students early in the semester
    2. **Personalized Support**: Provide tailored recommendations for each student
    3. **Data-Driven Decisions**: Use ML and analytics for objective assessment
    4. **Actionable Insights**: Generate clear, actionable improvement plans
    5. **Track Progress**: Monitor student improvement over time
    
    ---
    
    ## 🛠️ Technology Stack
    
    | Component | Technology |
    |-----------|-----------|
    | Frontend/UI | **Streamlit** |
    | Machine Learning | **Scikit-learn** |
    | Data Processing | **Pandas, NumPy** |
    | Data Visualization | **Plotly** |
    | Report Generation | **ReportLab** |
    | Database | **SQLite3** |
    | Model Serialization | **Joblib** |
    | Development | **Python 3.8+** |
    | Deployment | **Streamlit Cloud** |
    
    ---
    
    ## 📊 Features
    
    ### 1. Manual Student Entry
    - Teachers can manually enter student details
    - Easy-to-use form interface
    - Real-time validation
    
    ### 2. Intelligent Prediction
    - **ML-Based**: Uses trained scikit-learn model
    - **Rule-Based**: Implements academic risk scoring logic
    - **Combined**: Averages both approaches for robustness
    
    ### 3. Risk Scoring
    - Generates risk score from 0-100
    - Categorized into 3 levels:
      - 🟢 Low Risk (0-30)
      - 🟡 Medium Risk (30-60)
      - 🔴 High Risk (60-100)
    
    ### 4. Personalized Recommendations
    - Attendance improvement strategies
    - Academic performance tips
    - Time management advice
    - Health & wellness suggestions
    - Motivational messages
    
    ### 5. Student Database
    - SQLite database for persistent storage
    - Records all predictions and assessments
    - Search and filter capabilities
    - CSV export functionality
    
    ### 6. Analytics Dashboard
    - Risk distribution charts
    - Performance metrics visualization
    - High-risk student tracking
    - Comparative analysis
    
    ### 7. PDF Report Generation
    - Professional PDF reports
    - Student details and predictions
    - Risk factors and recommendations
    - Action plans with timelines
    - Exportable for emails/records
    
    ---
    
    ## 🔄 Workflow
    
    ```
    CSV Dataset (Training Data)
           ↓
    Train in Google Colab
           ↓
    Save model.pkl
           ↓
    Load in Streamlit App
           ↓
    Manual Student Entry (Teacher)
           ↓
    ML + Rule-Based Prediction
           ↓
    Risk Assessment
           ↓
    Personalized Recommendations
           ↓
    PDF Report Generation
    ```
    
    ---
    
    ## 📈 Risk Scoring Logic
    
    ### Rule-Based Factors:
    - **Attendance < 60%** → +30 points
    - **Quiz Average < 50** → +20 points
    - **Assignment Average < 50** → +15 points
    - **Study Hours < 2/day** → +15 points
    - **Previous GPA < 2.5** → +20 points
    - **Sleep Hours < 6/day** → +5 points
    - **Internet Usage > 6 hours/day** → +5 points
    - **Class Participation < 50%** → +5 points
    
    ---
    
    ## 📋 Input Features
    
    The system considers 12 key factors:
    
    1. **Attendance %** - Class attendance percentage
    2. **Quiz Average** - Average quiz scores
    3. **Assignment Average** - Average assignment scores
    4. **Midterm Marks** - Midterm exam performance
    5. **Study Hours** - Daily study time
    6. **Sleep Hours** - Daily sleep duration
    7. **Internet Usage** - Daily internet/social media time
    8. **Previous GPA** - Cumulative GPA
    9. **Class Participation** - In-class engagement
    10. **Student Name** - For identification
    11. **Roll Number** - Student ID
    12. **Gender** - Demographics
    
    ---
    
    ## 🎯 Recommendation Categories
    
    - 📚 **Attendance** - Strategies to improve class attendance
    - 📖 **Academic Performance** - Tips for exams and assignments
    - ⏰ **Time Management** - Scheduling and productivity tips
    - 💚 **Health & Well-being** - Sleep, exercise, stress management
    - 🎯 **General Tips** - Motivational messages and action plans
    
    ---
    
    ## 🚀 How to Use
    
    ### Step 1: Data Collection
    - Teachers fill in student data using the **Manual Prediction** page
    
    ### Step 2: Prediction
    - System analyzes data and generates risk prediction
    
    ### Step 3: Review
    - Teachers review risk level, factors, and recommendations
    
    ### Step 4: Take Action
    - Follow personalized recommendations and action plans
    
    ### Step 5: Monitor
    - Track student progress using **Analytics Dashboard**
    
    ### Step 6: Report
    - Generate and download PDF reports for records/parent meetings
    
    ---
    
    ## 📊 Database Schema
    
    **Table: student_records**
    
    | Column | Type | Description |
    |--------|------|-------------|
    | id | INTEGER | Primary key |
    | student_name | TEXT | Student's full name |
    | roll_number | TEXT | Student ID (unique) |
    | gender | TEXT | Student gender |
    | attendance_percent | REAL | Attendance % |
    | quiz_average | REAL | Average quiz score |
    | assignment_average | REAL | Average assignment score |
    | midterm_marks | REAL | Midterm exam marks |
    | study_hours_per_day | REAL | Daily study hours |
    | sleep_hours | REAL | Daily sleep hours |
    | internet_usage_hours | REAL | Daily internet usage |
    | previous_gpa | REAL | Cumulative GPA |
    | class_participation | REAL | Class participation % |
    | predicted_risk_level | TEXT | Risk level prediction |
    | risk_score | REAL | Risk score (0-100) |
    | created_date | TIMESTAMP | Record creation date |
    | updated_date | TIMESTAMP | Record update date |
    
    ---
    
    ## 🔐 Future Enhancements
    
    - [ ] Integrate with Excel/Google Sheets for bulk uploads
    - [ ] Email notifications for high-risk alerts
    - [ ] Student login portal to view their own assessments
    - [ ] Parent notification system
    - [ ] Progress tracking over multiple semesters
    - [ ] Automated intervention workflow
    - [ ] Integration with Learning Management Systems (LMS)
    - [ ] Advanced ML models (Random Forest, Gradient Boosting)
    - [ ] Predictive analysis for course recommendations
    
    ---
    
    ## ⚙️ Installation & Deployment
    
    ### Local Setup
    ```bash
    git clone <repo-url>
    cd EduShield-AI
    pip install -r requirements.txt
    streamlit run app.py
    ```
    
    ### Streamlit Cloud Deployment
    1. Push code to GitHub
    2. Connect to Streamlit Cloud
    3. Deploy in 1 click
    4. Share public URL with users
    
    ---
    
    ## 📝 License & Credits
    
    **Project**: EduShield AI Lite
    **Version**: 1.0
    **Status**: Active Development
    **Developed**: For Educational Technology
    
    ---
    
    ## 📧 Support
    
    For issues, suggestions, or feedback:
    - Open an issue on GitHub
    - Contact the development team
    - Check documentation wiki
    
    ---
    
    ### 🙏 Thank You!
    
    Thank you for using **EduShield AI Lite**. Together, we can help students succeed! 🎓
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
    <p>🛡️ <strong>EduShield AI Lite</strong> | Student Academic Risk Assessment System</p>
    <p style='font-size: 0.9rem;'>Built with ❤️ using Streamlit | Powered by Python & ML</p>
    </div>
    """,
    unsafe_allow_html=True
)
