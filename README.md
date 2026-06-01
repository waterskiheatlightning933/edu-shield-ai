# 🛡️ EduShield AI Lite - Student Academic Risk Assessment

A comprehensive Streamlit-based web application that uses machine learning and rule-based analysis to predict student academic risk levels and provide personalized intervention recommendations.

## ✨ Features

- ✅ **Manual Student Entry**: Teachers manually enter student details through an easy form
- ✅ **ML + Rule-Based Prediction**: Combines scikit-learn model with custom risk scoring logic
- ✅ **Risk Assessment**: Generates risk scores (0-100) and categorizes as Low/Medium/High
- ✅ **Student Database**: SQLite database for persistent storage of all assessments
- ✅ **Personalized Recommendations**: Tailored improvement strategies for each student
- ✅ **Analytics Dashboard**: Visualize risk distribution, trends, and high-risk students
- ✅ **PDF Report Generation**: Professional reports for records and parent meetings
- ✅ **Search & Filter**: Find and manage student records easily
- ✅ **CSV Export**: Download student data for further analysis

## 🎯 Risk Levels

| Level | Score Range | Status | Color |
|-------|-------------|--------|-------|
| 🟢 Low Risk | 0-30 | Performing well | Green |
| 🟡 Medium Risk | 30-60 | Needs attention | Orange |
| 🔴 High Risk | 60-100 | Urgent intervention | Red |

## 📊 Project Structure

```
EduShield-AI/
│
├── app.py                           # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── model/
│   └── student_risk_model.pkl      # Trained ML model (to be added)
│
├── data/
│   └── student_dataset.csv         # Training dataset (to be added)
│
├── utils/
│   ├── predictor.py                # ML inference & risk scoring
│   ├── recommendations.py          # Personalized recommendations engine
│   ├── database.py                 # SQLite database operations
│   └── report_generator.py         # PDF report generation
│
└── student_records.db              # SQLite database (auto-created)
```

## 🚀 Quick Start

### 1. Clone or Download Project
```bash
cd EduShield-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📋 Pages Overview

### 1. 🏠 Home
- System overview and introduction
- Key statistics and features
- Quick start guide
- Navigation help

### 2. 📝 Manual Prediction
- **Main feature** for teacher usage
- Form to enter student details
- Real-time prediction
- Risk factors identification
- Personalized recommendations
- Action plan generation
- PDF report download

**Input Fields:**
- Student Name & Roll Number
- Gender & Class Level
- Attendance %
- Quiz Average, Assignment Average, Midterm Marks
- Study Hours/Day, Sleep Hours, Internet Usage
- Previous GPA, Class Participation

### 3. 📊 Student Records
- View all student assessments
- Search by name or roll number
- Filter by risk level
- View detailed record information
- Delete records
- Export to CSV

### 4. 📈 Analytics Dashboard
- Risk distribution pie chart
- Attendance vs Risk scatter plot
- GPA distribution histogram
- Quiz average distribution
- High-risk student list
- Attendance by risk level box plot
- Key metrics and statistics

### 5. 📋 PDF Report
- Generate professional PDF reports
- Select student by roll number
- Export for records or parent meetings
- Includes all prediction details and recommendations

### 6. ℹ️ About Project
- Comprehensive project documentation
- Technology stack details
- Feature descriptions
- Workflow overview
- Database schema
- Future enhancements

## 🎓 Input Features (12 Factors)

1. **Attendance %** - Class attendance percentage (0-100)
2. **Quiz Average** - Average quiz scores (0-100)
3. **Assignment Average** - Average assignment scores (0-100)
4. **Midterm Marks** - Midterm exam performance (0-100)
5. **Study Hours/Day** - Daily study time in hours (0-12)
6. **Sleep Hours/Day** - Daily sleep in hours (0-12)
7. **Internet Usage/Day** - Daily internet/social media usage (0-24)
8. **Previous GPA** - Cumulative GPA (0-4.0)
9. **Class Participation** - In-class engagement percentage (0-100)
10. **Gender** - Categorical (Male/Female/Other)
11. **Student Name** - For identification
12. **Roll Number** - Student ID (unique)

## 🔮 Risk Prediction Logic

### Rule-Based Scoring:
```
Risk Score = 0 (base)

IF Attendance < 60%      → +30 points
IF Attendance < 75%      → +15 points

IF Quiz Average < 50     → +20 points
IF Quiz Average < 65     → +10 points

IF Assignment Avg < 50   → +15 points
IF Assignment Avg < 65   → +8 points

IF Study Hours < 2/day   → +15 points
IF Study Hours < 3/day   → +8 points

IF Previous GPA < 2.5    → +20 points
IF Previous GPA < 3.0    → +10 points

IF Sleep Hours < 6/day   → +5 points

IF Internet > 6 hours    → +5 points

IF Class Participation < 50% → +5 points

Final Score = min(Total, 100)
```

### ML Model Integration:
- Loads pre-trained scikit-learn model
- Generates independent ML prediction
- Averages with rule-based score for final decision
- Falls back to rule-based only if model unavailable

## 💡 Recommendation Categories

### 📚 Attendance
- Targets students with low class attendance
- Suggests specific attendance targets
- Provides meeting strategies

### 📖 Academic Performance
- Quiz improvement strategies
- Assignment completion tips
- Exam preparation guidance
- Tutoring recommendations

### ⏰ Time Management
- Study schedule creation
- Pomodoro technique tips
- Distraction elimination strategies
- Priority management

### 💚 Health & Well-being
- Sleep optimization (7-8 hours target)
- Screen time management
- Stress management tips
- Balanced lifestyle advice

### 🎯 General Tips
- Motivational messages
- Action plans
- Study group suggestions
- Mentor recommendations

## 📊 Database

**SQLite Database**: `student_records.db` (auto-created)

**Table**: `student_records`
- Stores all student assessments
- Fields: Name, Roll #, Gender, Performance metrics, Risk level, Risk score, Timestamps
- Supports CRUD operations (Create, Read, Update, Delete)
- Search and filtering capabilities

## 🛠️ Technologies Used

| Purpose | Technology |
|---------|-----------|
| **Web Framework** | Streamlit |
| **ML Library** | Scikit-learn |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly |
| **Database** | SQLite3 |
| **PDF Generation** | ReportLab |
| **Model Serialization** | Joblib |
| **Language** | Python 3.8+ |

## 📥 Requirements

All dependencies are in `requirements.txt`:

```
streamlit
pandas
numpy
scikit-learn
joblib
plotly
reportlab
sqlite3  # Built-in with Python
```

## 🔧 Setup Instructions

### Step 1: Environment Setup
```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Add Model & Data
- Place trained model in `model/student_risk_model.pkl`
- Place training dataset in `data/student_dataset.csv`
- (App works without these - it uses rule-based scoring by default)

### Step 3: Run Application
```bash
streamlit run app.py
```

## 🚀 How to Train the Model

### In Google Colab:

1. Use the `xAPI-Edu-Data` dataset from Kaggle
2. Use this prompt in GitHub Copilot:

```
Create a complete machine learning training notebook for student academic risk prediction.

Requirements:
- Load CSV with pandas
- Clean missing values
- Encode categorical columns
- Scale numerical columns
- Create target labels: Low Risk, Medium Risk, High Risk
- Train Logistic Regression and Random Forest models
- Compare accuracy, precision, recall, F1-score
- Save the best model using joblib as student_risk_model.pkl
```

3. Download `student_risk_model.pkl`
4. Place in `model/` folder

## 📝 Usage Workflow

```
1. Teacher enters student details in "Manual Prediction" page
        ↓
2. System processes and analyzes data
        ↓
3. Prediction results displayed with:
   - Risk level (Low/Medium/High)
   - Risk score (0-100)
   - Contributing factors
        ↓
4. Personalized recommendations shown
        ↓
5. Action plan provided with timelines
        ↓
6. PDF report available for download
        ↓
7. Record saved to database
        ↓
8. Teacher can track progress in Analytics
```

## 🎯 Use Cases

### For Teachers:
- Identify struggling students early
- Get actionable recommendations to help
- Generate reports for parent meetings
- Track student improvement over time
- Prioritize intervention efforts

### For Administrators:
- Analyze class-level performance trends
- Identify high-risk cohorts
- Allocate tutoring resources effectively
- Monitor intervention outcomes
- Generate reports for stakeholders

### For Students:
- Understand their academic standing
- Get personalized improvement suggestions
- View progress dashboard
- Receive motivational feedback

## 🔒 Data Privacy

- All data stored locally in SQLite
- No cloud sync unless explicitly configured
- Records can be deleted anytime
- Teacher-controlled access

## 📞 Troubleshooting

### "Model not found" message
- App still works with rule-based scoring
- Place trained model in `model/student_risk_model.pkl`
- See "Train the Model" section above

### Database errors
- Delete `student_records.db` and restart app
- Database will be recreated

### Streamlit not installed
```bash
pip install streamlit
```

### Port already in use
```bash
streamlit run app.py --logger.level=debug --server.port 8502
```

## 🌐 Deployment

### Deploy on Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Connect GitHub account
4. Select this repository
5. Deploy in 1 click!

### Share URL
Public URL: `https://share.streamlit.io/username/repo`

## 📊 Sample Data

To test the app, try these sample students:

**Sample 1: High Risk**
- Attendance: 40%, Quiz: 35, Assignment: 40
- Midterm: 30, Study: 1 hr/day, Previous GPA: 2.0
- Sleep: 5 hrs, Internet: 8 hrs, Participation: 30%

**Sample 2: Medium Risk**
- Attendance: 70%, Quiz: 60, Assignment: 65
- Midterm: 60, Study: 2.5 hrs/day, Previous GPA: 2.8
- Sleep: 6.5 hrs, Internet: 5 hrs, Participation: 60%

**Sample 3: Low Risk**
- Attendance: 95%, Quiz: 85, Assignment: 88
- Midterm: 82, Study: 3.5 hrs/day, Previous GPA: 3.5
- Sleep: 8 hrs, Internet: 3 hrs, Participation: 90%

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open-source and available for educational use.

## 🙏 Credits

Built with:
- **Streamlit** - Interactive web framework
- **Scikit-learn** - Machine learning library
- **Plotly** - Data visualization
- **ReportLab** - PDF generation
- **SQLite** - Lightweight database

## 📞 Support

For issues or questions:
1. Check the **About Project** page in app
2. Review this README
3. Check Streamlit documentation
4. Raise GitHub issues

## 🚀 Future Roadmap

- [ ] Bulk import from Excel/CSV
- [ ] Email alerts for high-risk students
- [ ] Student login portal
- [ ] Parent notification system
- [ ] Multi-semester tracking
- [ ] Advanced ML models
- [ ] LMS integration
- [ ] Mobile app

---

**🛡️ EduShield AI Lite** - Helping students succeed through intelligent risk assessment! 🎓
