# 🏢 Job Dekho - Smart Job Portal with Text-to-Speech

An intelligent job matching platform built with Streamlit, featuring advanced text-to-speech functionality for accessibility and enhanced user experience.

## ✨ Features

### 🎓 For Students
- **Smart Registration**: Complete profile with skills, CGPA, and branch information
- **Intelligent Job Matching**: AI-powered algorithm matches you with suitable jobs
- **Automatic Shortlisting**: Get instantly shortlisted for compatible positions
- **Resume Management**: Upload and manage your resume (PDF/DOCX)
- **Application Tracking**: Monitor your application status in real-time
- **🔊 Voice Assistance**: Listen to job descriptions and notifications

### 🏢 For Companies
- **Easy Job Posting**: Post jobs with detailed requirements
- **Smart Candidate Filtering**: Automatic matching based on skills and qualifications
- **Application Management**: Review and update candidate statuses
- **Dashboard Analytics**: Track job performance and application metrics
- **🔊 Voice Interface**: Accessibility features for all interactions

### 🤖 Smart Features
- **Compatibility Scoring**: See how well you match each job (0-100%)
- **Automatic Shortlisting**: Algorithm determines if candidates meet criteria
- **Real-time Updates**: Instant notifications for status changes
- **Accessibility**: Full text-to-speech support for inclusive design

## 🚀 Quick Start

### Option 1: Easy Start (Recommended)
1. **Double-click** `start_job_dekho.bat`
2. **Wait** for the application to load in your browser
3. **Enjoy!** The app will open at `http://localhost:8501`

### Option 2: Command Line
```bash
# Activate virtual environment
job_dekho_env\Scripts\activate

# Run the application
streamlit run streamlit_app.py
```

### Option 3: Python Script
```bash
python run_streamlit.py
```

## 📋 System Requirements

### Software Requirements
- **Python 3.7+** (Currently using Python 3.14)
- **Windows OS** (for TTS functionality)
- **Web Browser** (Chrome, Firefox, Edge, Safari)
- **Audio Output** (Speakers/Headphones for TTS)

### Hardware Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 500MB free space
- **Network**: Internet connection for initial setup
- **Audio**: Sound card and speakers/headphones

## 🛠️ Technical Stack

### Core Technologies
- **Framework**: Streamlit 1.28.1
- **Database**: SQLite with SQLAlchemy ORM
- **TTS Engine**: pyttsx3 2.99
- **UI Components**: Bootstrap-style Streamlit components
- **Charts**: Altair for data visualization

### Key Libraries
```
streamlit==1.28.1          # Web framework
pyttsx3==2.99              # Text-to-speech engine
SQLAlchemy==2.0.44         # Database ORM
bcrypt==5.0.0              # Password hashing
pandas==2.3.3              # Data manipulation
altair==5.5.0              # Data visualization
pillow==11.3.0             # Image processing
```

## 📁 Project Structure

```
Job_Dekho/
├── 📄 streamlit_app.py           # Main Streamlit application
├── 📄 streamlit_models.py        # Database models
├── 📄 tts_utils.py               # Text-to-speech utilities
├── 📄 matching_algorithm.py      # Job matching logic
├── 📄 run_streamlit.py           # Application launcher
├── 📄 start_job_dekho.bat        # Windows batch launcher
├── 📄 README_STREAMLIT.md        # This documentation
├── 📄 requirements_streamlit.txt  # Python dependencies
├── 🗂️ job_dekho_env/             # Virtual environment
├── 🗂️ templates/ (old)           # Flask templates (legacy)
├── 📄 job_dekho_streamlit.db     # SQLite database
└── 🗂️ uploads/ (legacy)          # File uploads (for future use)
```

## 🎯 How to Use

### Getting Started
1. **Launch** the application using any of the quick start methods
2. **Choose your role**: Student or Company
3. **Register** with your details
4. **Complete your profile** with relevant information

### For Students
1. **Register** with academic information (CGPA, Branch, Skills)
2. **Upload your resume** for better matching
3. **Browse jobs** on your dashboard
4. **Check compatibility** scores for each job
5. **Apply** to jobs that interest you
6. **Track** your application status
7. **🔊 Use TTS** to listen to job descriptions

### For Companies
1. **Register** with company information
2. **Complete company profile** with details
3. **Post jobs** with specific requirements
4. **Review applications** as they come in
5. **Update candidate status** (Applied → Shortlisted → Selected)
6. **🔊 Use voice features** to navigate efficiently

## 🔊 Text-to-Speech Features

### What Can Be Read Aloud?
- ✅ **Page Titles**: Announces current page when you navigate
- ✅ **Welcome Messages**: Personalized greetings
- ✅ **Job Descriptions**: Complete job details including requirements
- ✅ **Candidate Information**: Student profiles and qualifications
- ✅ **Notifications**: Success, error, and warning messages
- ✅ **Statistics**: Dashboard metrics and numbers
- ✅ **Instructions**: Page descriptions and help text

### TTS Controls
- **🔊 Listen Buttons**: Click to hear specific content
- **🛑 Stop Speech**: Stop current audio playback
- **⚙️ TTS Test**: Test speech functionality in sidebar
- **🎵 Auto-Announcements**: Automatic notifications

### TTS Settings
- **Speed**: 150 words per minute (optimized)
- **Volume**: 80% (comfortable listening)
- **Voice**: System default voice
- **Language**: English

## 🤖 Intelligent Matching Algorithm

### How It Works
The matching algorithm evaluates candidates based on three criteria:

1. **CGPA Match (40 points)**
   - Must meet minimum requirement
   - Higher CGPA = Higher score

2. **Branch Match (30 points)**  
   - Exact branch match required
   - "Any" branch accepts all students

3. **Skills Match (30 points)**
   - At least one required skill must match
   - More matching skills = Higher score

### Scoring System
- **70-100%**: 🎯 Excellent Match (Green)
- **50-69%**: ⚠️ Good Match (Yellow) 
- **0-49%**: ℹ️ Partial Match (Blue)

### Automatic Shortlisting
- **100% Match**: Automatically shortlisted ✨
- **<100% Match**: Marked as "Applied" for manual review

## 🗄️ Database Schema

### Tables
```sql
users                    # User accounts
├── id (Primary Key)
├── email (Unique)
├── password_hash
├── role (student/company)
└── created_at

students                 # Student profiles  
├── id (Primary Key)
├── user_id (Foreign Key)
├── name, roll_number
├── cgpa, branch, skills
└── resume_path

companies               # Company profiles
├── id (Primary Key) 
├── user_id (Foreign Key)
├── name, industry
└── description, website

jobs                    # Job postings
├── id (Primary Key)
├── company_id (Foreign Key)
├── title, description
├── min_cgpa, required_branch
├── required_skills, salary
└── location, is_active

applications           # Job applications
├── id (Primary Key)
├── student_id, job_id (Foreign Keys)
├── status (Applied/Shortlisted/Rejected/Selected)
└── applied_at, updated_at
```

## 🔧 Advanced Configuration

### Customizing TTS Settings
Edit `tts_utils.py`:
```python
# Change speech rate (words per minute)
self.engine.setProperty('rate', 180)  # Default: 150

# Change volume (0.0 to 1.0)
self.engine.setProperty('volume', 0.9)  # Default: 0.8

# Change voice (if multiple available)
voices = self.engine.getProperty('voices')
self.engine.setProperty('voice', voices[1].id)  # Use second voice
```

### Database Configuration
Edit `streamlit_models.py`:
```python
# Change database location
DATABASE_URL = "sqlite:///custom_database.db"

# Use PostgreSQL (requires psycopg2)
DATABASE_URL = "postgresql://user:pass@localhost/dbname"

# Use MySQL (requires pymysql)
DATABASE_URL = "mysql+pymysql://user:pass@localhost/dbname"
```

### UI Customization
Edit `streamlit_app.py`:
```python
# Change page configuration
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="🎯",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)
```

## 🚨 Troubleshooting

### Common Issues

#### TTS Not Working
```
❌ Problem: "TTS not available" message
✅ Solutions:
   • Check Windows audio settings
   • Install/update Windows Speech Platform
   • Try running as administrator
   • Restart the application
```

#### Database Errors
```
❌ Problem: Database connection failed
✅ Solutions:
   • Delete job_dekho_streamlit.db and restart
   • Check file permissions
   • Ensure SQLite is properly installed
```

#### Import Errors
```
❌ Problem: ModuleNotFoundError
✅ Solutions:
   • Activate virtual environment first
   • pip install -r requirements_streamlit.txt
   • Check Python version compatibility
```

#### Browser Issues
```
❌ Problem: Page doesn't load
✅ Solutions:
   • Clear browser cache
   • Try different browser
   • Check URL: http://localhost:8501
   • Restart application
```

#### Performance Issues
```
❌ Problem: Application runs slowly
✅ Solutions:
   • Close unnecessary browser tabs
   • Increase system RAM
   • Clear database if too large
   • Restart computer
```

### Getting Help
1. **Check Console**: Look at terminal output for error messages
2. **Test Components**: Use TTS test in sidebar
3. **Database Reset**: Delete .db file to start fresh
4. **Restart**: Close and reopen application
5. **System Requirements**: Verify your system meets requirements

## 🔄 Version History

### v2.0.0 - Streamlit with TTS (Current)
- ✨ **NEW**: Full Streamlit web interface
- ✨ **NEW**: Integrated text-to-speech functionality
- ✨ **NEW**: Voice-guided navigation
- ✨ **NEW**: Enhanced accessibility features
- 🔧 **IMPROVED**: Modern, responsive UI
- 🔧 **IMPROVED**: Better database integration
- 🔧 **IMPROVED**: Enhanced matching algorithm

### v1.0.0 - Flask Version (Legacy)
- ⚡ Basic Flask web application
- ⚡ HTML templates with Bootstrap
- ⚡ SQLite database
- ⚡ Job matching algorithm

## 🎉 What's Next?

### Planned Features
- 📱 **Mobile App**: React Native application
- 🌐 **Multi-language**: Support for multiple languages
- 📊 **Advanced Analytics**: Detailed reporting and insights
- 💬 **Chat System**: Communication between students and companies
- 🔔 **Email Notifications**: Automated email updates
- 🎨 **Themes**: Dark mode and custom themes
- 📈 **Machine Learning**: Enhanced matching with ML
- 🔒 **Advanced Security**: Two-factor authentication

### Contribute
This project is open for contributions! Areas where you can help:
- 🐛 Bug fixes and improvements
- 🎨 UI/UX enhancements
- 🔊 TTS improvements
- 📱 Mobile responsiveness
- 🌐 Internationalization
- 📊 Analytics and reporting
- 🔒 Security enhancements

## 📄 License

This project is created for educational and development purposes. Feel free to use, modify, and distribute according to your needs.

## 🙏 Acknowledgments

- **Streamlit Team**: For the amazing framework
- **pyttsx3 Developers**: For the TTS library
- **SQLAlchemy Team**: For the excellent ORM
- **Python Community**: For the incredible ecosystem

---

<div align="center">

**🏢 Job Dekho - Connecting Talent with Opportunity through Smart Technology & Voice Assistance**

*Built with ❤️ using Streamlit, Python, and Text-to-Speech*

[🚀 Start Application](#-quick-start) • [📖 Documentation](#-features) • [🔊 TTS Guide](#-text-to-speech-features) • [🤖 Matching Algorithm](#-intelligent-matching-algorithm)

</div>