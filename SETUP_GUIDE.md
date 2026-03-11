# Job Dekho - Complete Setup Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Features Overview](#features-overview)
5. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System:** Windows 10/11 (for TTS features)
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 500MB free space
- **Internet:** Required for initial setup and package installation

### Software Prerequisites
- Python 3.8+ installed ([Download](https://www.python.org/downloads/))
- pip (comes with Python)
- Command Prompt or PowerShell

## Installation Steps

### Step 1: Verify Python Installation
Open Command Prompt or PowerShell and run:
```bash
python --version
```
You should see Python 3.8 or higher.

### Step 2: Navigate to Project Directory
```bash
cd C:\Users\PC\Desktop\Job_Dekho
```

### Step 3: Install Dependencies
```bash
pip install -r requirements_complete.txt
```

This will install:
- Flask (web framework)
- Streamlit (modern UI framework)
- SQLAlchemy (database ORM)
- pyttsx3 (text-to-speech)
- bcrypt (password hashing)
- And other required packages

**Expected installation time:** 2-5 minutes (depending on internet speed)

### Step 4: Verify Installation
```bash
python -c "import flask, streamlit, pyttsx3; print('✅ All packages installed!')"
```

## Running the Application

### Option 1: Interactive Menu (Recommended)
```bash
python start.py
```

This will display a menu where you can choose:
1. **Flask Web Application** - Traditional web interface
2. **Streamlit Application** - Modern UI with Text-to-Speech
3. **Standalone Demo** - See features without web interface

### Option 2: Direct Launch

#### Flask Version
```bash
python app.py
```
- Opens at: http://127.0.0.1:5000
- Traditional web interface
- Full CRUD functionality
- Resume upload
- Session-based authentication

#### Streamlit Version (with TTS)
```bash
streamlit run streamlit_app.py
```
- Opens at: http://localhost:8501
- Modern, interactive UI
- **Text-to-Speech features:**
  - Voice announcements for navigation
  - Read job descriptions aloud
  - Speak candidate information
  - Success/error message narration
- Real-time updates

#### Standalone Demo
```bash
python demo_job_dekho.py
```
- Console-based demonstration
- Shows matching algorithm
- Tests TTS functionality
- Creates sample data

## Features Overview

### For Students 👨‍🎓
1. **Registration & Profile**
   - Create account with academic details
   - Upload resume (PDF/DOCX)
   - Manage skills and qualifications

2. **Job Browsing**
   - View all available jobs
   - See match percentage for each job
   - Filter by compatibility

3. **Application Process**
   - One-click apply
   - Automatic shortlisting based on eligibility
   - Track application status

4. **Dashboard**
   - View all applications
   - Statistics (total applied, shortlisted)
   - Application history

### For Companies 🏢
1. **Company Profile**
   - Company information
   - Industry details
   - Contact information

2. **Job Posting**
   - Post job openings
   - Define requirements (CGPA, branch, skills)
   - Specify salary and location

3. **Application Management**
   - View all applications
   - Update candidate status
   - Filter by job posting

4. **Dashboard**
   - Statistics (jobs posted, applications received)
   - Shortlisted candidates
   - Hiring pipeline overview

### Smart Matching Algorithm 🎯
The system automatically calculates match scores based on:
- **CGPA (40%)**: Student's CGPA vs. minimum requirement
- **Branch (30%)**: Student's branch vs. required branch
- **Skills (30%)**: Matching skills between student and job

**Auto-Shortlisting:**
- Students meeting all criteria (100% match) are automatically shortlisted
- Others are marked as "Applied" for company review

### Text-to-Speech Features 🔊 (Streamlit Version)
- **Page Navigation:** Announces current page
- **Job Descriptions:** Read aloud button for each job
- **Notifications:** Voice alerts for success/error messages
- **Candidate Info:** Speak candidate details
- **Controls:** Stop, pause, and customize voice settings

## Troubleshooting

### Issue: "Module not found" errors
**Solution:**
```bash
pip install -r requirements_complete.txt
```

### Issue: Port already in use
**Solution for Flask:**
Edit `app.py`, change the port:
```python
app.run(debug=True, port=5001)  # Changed from 5000
```

**Solution for Streamlit:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Issue: TTS not working
**Possible causes:**
1. **Windows only**: TTS requires Windows OS with SAPI
2. **Missing package**: Run `pip install pyttsx3 pywin32`
3. **Audio settings**: Check system volume and audio output

**Test TTS:**
```bash
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Test'); engine.runAndWait()"
```

### Issue: Database errors
**Solution:**
Delete and recreate database:
```bash
# For Flask
del instance\job_dekho.db

# For Streamlit
del job_dekho_streamlit.db

# Then restart the application - database will be recreated
```

### Issue: Resume upload fails
**Solution:**
1. Check `uploads/resumes/` directory exists
2. Ensure file is PDF or DOCX
3. Check file size (max 16MB)

### Issue: Python version incompatibility
**Solution:**
Check your Python version:
```bash
python --version
```
If below 3.8, upgrade Python from [python.org](https://www.python.org/downloads/)

## Database Management

### Viewing Database
Use DB Browser for SQLite:
1. Download from [sqlitebrowser.org](https://sqlitebrowser.org/)
2. Open `instance/job_dekho.db` or `job_dekho_streamlit.db`
3. Browse tables: users, students, companies, jobs, applications

### Resetting Database
**Flask:**
```bash
python -c "from app import app, db; app.app_context().push(); db.drop_all(); db.create_all(); print('Database reset!')"
```

**Streamlit:**
```bash
python -c "from streamlit_models import Base, engine; Base.metadata.drop_all(engine); Base.metadata.create_all(engine); print('Database reset!')"
```

## Additional Resources

### Project Structure
```
Job_Dekho/
├── start.py                    # Main launcher
├── requirements_complete.txt   # Dependencies
├── cleanup.py                  # Remove unused files
├── SETUP_GUIDE.md             # This file
│
├── Flask App:
│   ├── app.py
│   ├── models.py
│   ├── auth.py
│   ├── student.py
│   ├── company.py
│   └── templates/
│
├── Streamlit App:
│   ├── streamlit_app.py
│   ├── streamlit_models.py
│   └── tts_utils.py
│
└── Shared:
    ├── matching_algorithm.py
    └── demo_job_dekho.py
```

### Useful Commands
```bash
# Check installed packages
pip list

# Update a package
pip install --upgrade <package-name>

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Deactivate virtual environment
deactivate
```

## Support

### Getting Help
1. Check this guide first
2. Review README.md for features
3. Run demo to test functionality: `python demo_job_dekho.py`
4. Check troubleshooting section above

### Known Limitations
- TTS only works on Windows (uses SAPI)
- SQLite is for development (use PostgreSQL/MySQL for production)
- Resume preview not implemented (download only)
- Single-language support (English only)

## Next Steps

After successful setup:
1. ✅ Run `python start.py` and choose an option
2. ✅ Register a test student account
3. ✅ Register a test company account
4. ✅ Post a job as company
5. ✅ Apply for job as student
6. ✅ Test the matching algorithm
7. ✅ Try Text-to-Speech features (Streamlit version)

**Congratulations! Your Job Dekho installation is complete! 🎉**
