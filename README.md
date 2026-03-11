# Job Dekho - Intelligent Job Matching Portal

A dual-interface job matching platform with both Flask (traditional web) and Streamlit (modern with TTS) versions that connects students with companies through intelligent matching algorithms.

## Features

### For Students
- ✅ User registration and profile management
- ✅ Resume upload (PDF/DOCX)
- ✅ Browse and apply for jobs
- ✅ Intelligent automatic shortlisting based on:
  - CGPA requirements
  - Branch/department matching  
  - Skills compatibility
- ✅ View application status and history
- ✅ Dashboard with application statistics

### For Companies
- ✅ Company registration and profile management
- ✅ Post job openings with detailed requirements
- ✅ View and manage applications
- ✅ Update application status (Applied, Shortlisted, Rejected, Selected)
- ✅ Dashboard with hiring statistics
- ✅ Automatic candidate matching

### Technical Features
- ✅ **Dual Interface:** Choose between Flask (web) or Streamlit (with TTS)
- ✅ **Text-to-Speech:** Voice-guided interface in Streamlit version
- ✅ **SQLite Database:** Easy development and deployment
- ✅ **Responsive UI:** Bootstrap (Flask) / Modern Streamlit UI
- ✅ **Secure Authentication:** Password hashing with bcrypt/Werkzeug
- ✅ **File Upload:** Resume management system
- ✅ **Smart Matching:** Intelligent algorithm based on CGPA, branch, and skills
- ✅ **Auto-Shortlisting:** Automatic candidate qualification

### 🔊 Text-to-Speech Features (Streamlit Version)
- ✅ Voice announcements for page navigation
- ✅ Read job descriptions aloud
- ✅ Candidate information narration
- ✅ Success/error message announcements
- ✅ Custom TTS controls in sidebar
- ✅ Accessibility-friendly design

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Windows OS (for Text-to-Speech functionality)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd C:\Users\PC\Desktop\Job_Dekho
   ```

2. **Install all dependencies:**
   ```bash
   pip install -r requirements_complete.txt
   ```

3. **Run the application:**
   ```bash
   python start.py
   ```
   
   This will show you a menu to choose:
   - Flask Web Application
   - Streamlit Application (with TTS)
   - Standalone Demo

### Alternative: Run Directly

**Flask Version:**
```bash
python app.py
```
Access at: http://127.0.0.1:5000

**Streamlit Version (with Text-to-Speech):**
```bash
streamlit run streamlit_app.py
```
Access at: http://localhost:8501

**Standalone Demo:**
```bash
python demo_job_dekho.py
```

## Application Structure

```
Job_Dekho/
├── start.py               # Main startup script (choose Flask/Streamlit/Demo)
├── requirements_complete.txt  # All dependencies
│
├── Flask Application:
│   ├── app.py             # Main Flask application
│   ├── run.py             # Flask startup script
│   ├── models.py          # Flask database models
│   ├── auth.py            # Authentication routes
│   ├── student.py         # Student routes
│   ├── company.py         # Company routes
│   ├── templates/         # HTML templates
│   └── instance/          # SQLite database (job_dekho.db)
│
├── Streamlit Application:
│   ├── streamlit_app.py   # Main Streamlit app with TTS
│   ├── streamlit_models.py  # Streamlit database models
│   ├── tts_utils.py       # Text-to-Speech utilities
│   └── job_dekho_streamlit.db  # Streamlit database
│
├── Shared Components:
│   ├── matching_algorithm.py  # Intelligent matching logic
│   └── demo_job_dekho.py  # Standalone demonstration
│
└── uploads/resumes/       # Resume upload directory
```

## Usage Guide

### Getting Started

1. **Visit the homepage** at http://127.0.0.1:5000
2. **Choose your role:**
   - **Students:** Register to find and apply for jobs
   - **Companies:** Register to post jobs and find candidates

### For Students

1. **Register** with your academic details:
   - Email and password
   - Full name and roll number
   - CGPA and branch
   - Skills (comma-separated)

2. **Complete your profile** and **upload your resume**

3. **Browse available jobs** on your dashboard

4. **Apply for jobs** - the system will automatically determine if you're shortlisted based on:
   - Your CGPA vs. minimum requirement
   - Your branch vs. required branch
   - Your skills vs. required skills

5. **Track your applications** and their status

### For Companies

1. **Register** with your company details:
   - Email and password
   - Company name and industry
   - Description and contact information

2. **Post job openings** with detailed requirements:
   - Job title and description
   - Minimum CGPA required
   - Required branch/department
   - Required skills
   - Salary and location

3. **View applications** for your posted jobs

4. **Update application status** to manage your hiring pipeline

## Intelligent Matching Algorithm

The application includes a smart matching algorithm that automatically shortlists candidates based on:

1. **CGPA Matching** (40 points)
   - Must meet minimum CGPA requirement
   - Higher CGPA gets better score

2. **Branch Matching** (30 points)
   - Exact branch match required
   - Companies can specify "Any" for flexibility

3. **Skills Matching** (30 points)
   - At least one required skill must match
   - More matching skills = higher score

**Shortlisting:** Students with 100% match (all criteria met) are automatically shortlisted.

## Troubleshooting

### Common Issues

1. **Port already in use:**
   - Change the port in `run.py` or `app.py`
   - Kill any existing Python processes

2. **Database errors:**
   - Delete `instance/job_dekho.db` and restart the app
   - The database will be recreated automatically

3. **Template not found:**
   - Ensure all HTML files are in the `templates/` directory
   - Check file names match exactly (case-sensitive)

4. **File upload issues:**
   - Check that `uploads/resumes/` directory exists
   - Verify file permissions

## Development

### Database Reset
To reset the database:
```bash
python -c "from app import app, db; app.app_context().push(); db.drop_all(); db.create_all(); print('Database reset complete!')"
```

### Adding New Features
- Models: Edit `models.py`
- Routes: Add to appropriate blueprint files
- Templates: Add HTML files to `templates/`
- Static files: Add to `static/` directory

## Security Notes

⚠️ **For Development Only**
- Uses SQLite (not suitable for production)
- Simple secret key (change for production)
- No HTTPS (add SSL for production)
- Basic file upload validation

## License

This project is for educational/development purposes."# JOB_DEKHO-" 
"# JOB_DEKHO-" 
