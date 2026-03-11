# JOB DEKHO - Smart Job Matching Platform

A complete, production-ready job portal with intelligent matching algorithm, real-time application tracking, and comprehensive admin dashboard.

## 🚀 Features

### For Students
- ✅ **Smart Job Matching** - AI-powered algorithm matches based on CGPA, branch, and skills
- ✅ **Resume Upload** - PDF/DOCX support with secure storage
- ✅ **Browse Jobs** - Search and filter with real-time match scores
- ✅ **Apply with One Click** - Automatic eligibility checking
- ✅ **Real-Time Status Tracking** - Track application progress (Applied → Shortlisted → Selected)
- ✅ **Personalized Dashboard** - View stats and recommended jobs
- ✅ **Profile Management** - Update skills and qualifications

### For Companies
- ✅ **Post Jobs** - Create detailed job listings with requirements
- ✅ **Manage Applications** - View all applicants with match scores
- ✅ **Update Status** - Change application status in real-time
- ✅ **Smart Filtering** - See best-matched candidates first
- ✅ **Company Dashboard** - Analytics and hiring pipeline
- ✅ **Job Management** - Edit, activate/deactivate job postings

### For Admins
- ✅ **Comprehensive Dashboard** - Real-time statistics and analytics
- ✅ **User Management** - Activate/deactivate users, view all accounts
- ✅ **Data Analytics** - Success rates, top skills, hiring trends
- ✅ **Job Monitoring** - Oversee all job postings
- ✅ **Application Tracking** - Monitor all applications across platform
- ✅ **Search & Filter** - Find users, companies, jobs, applications quickly

### Technical Features
- ✅ **MySQL Database** - Production-ready with SQLAlchemy ORM
- ✅ **Secure Authentication** - Password hashing, session management
- ✅ **Responsive Design** - Bootstrap 5, mobile-friendly
- ✅ **Real-Time Updates** - AJAX calls for dynamic content
- ✅ **RESTful API** - JSON endpoints for stats and data
- ✅ **Resume Analysis** - Extract CGPA and skills from resumes
- ✅ **File Upload System** - Secure resume storage
- ✅ **Advanced Search** - Filter by location, job type, status
- ✅ **Export Functionality** - CSV export for data

## 📋 Requirements

- Python 3.8+
- MySQL 5.7+ or MariaDB (optional, falls back to SQLite)
- pip (Python package manager)

## 🛠️ Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Database (Optional)

**For MySQL:**
```bash
# Create database
mysql -u root -p
CREATE DATABASE job_dekho;
EXIT;

# Set environment variable
set DATABASE_URL=mysql+pymysql://root:your_password@localhost/job_dekho
```

**For SQLite (Default):**
No configuration needed! The system will automatically use SQLite.

### Step 3: Initialize Database

```bash
python init_db.py
```

This creates all tables and adds sample data including:
- 1 Admin account
- 5 Sample students
- 4 Sample companies
- 7 Sample job postings
- Sample applications

### Step 4: Run the Application

```bash
python app.py
```

Visit: **http://127.0.0.1:5000**

## 👥 Test Accounts

### Admin
- **Email:** admin@jobdekho.com
- **Password:** admin123

### Students (all have password: `student123`)
- rahul.sharma@student.com - CGPA 8.5, CS
- priya.patel@student.com - CGPA 9.2, CS
- amit.kumar@student.com - CGPA 7.8, Electronics
- sneha.reddy@student.com - CGPA 8.9, CS
- vikram.singh@student.com - CGPA 7.5, Mechanical

### Companies (all have password: `company123`)
- hr@techcorp.com - TechCorp Solutions
- careers@innovate.com - Innovate Systems
- jobs@datatech.com - DataTech Analytics
- recruit@cloudnine.com - CloudNine Technologies

## 🎯 How It Works

### Matching Algorithm

The intelligent matching algorithm evaluates candidates on 3 criteria:

1. **CGPA Matching (40 points)**
   - Must meet minimum CGPA requirement
   - Extra points for higher CGPA

2. **Branch Matching (30 points)**
   - Must match required branch/department
   - Companies can specify "Any" for all branches

3. **Skills Matching (30 points)**
   - At least one required skill must match
   - More matching skills = higher score

**Total Score:** 100 points
- **90-100:** Excellent match → Auto-shortlisted
- **75-89:** Good match → Pending review
- **60-74:** Meets requirements → Pending review
- **<60:** Not eligible

### Application Statuses

1. **Applied** - Initial submission, awaiting review
2. **Shortlisted** - Candidate selected for next round
3. **Selected** - Final selection made
4. **Rejected** - Application rejected

## 📁 Project Structure

```
Job_Dekho/
├── app.py                      # Main Flask application
├── models.py                   # Database models (SQLAlchemy)
├── init_db.py                  # Database initialization
├── auth.py                     # Authentication blueprint
├── student.py                  # Student portal blueprint
├── company.py                  # Company portal blueprint
├── admin.py                    # Admin dashboard blueprint
├── matching_algorithm.py       # Job matching logic
├── requirements.txt            # Python dependencies
├── SETUP_PROJECT.py           # Auto-generates all files
├──
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Homepage
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── admin/                 # Admin templates
│   ├── student/               # Student templates
│   └── company/               # Company templates
├──
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── main.js            # JavaScript functions
└──
└── uploads/
    └── resumes/               # Resume storage
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional):

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://user:pass@localhost/job_dekho
```

### MySQL Setup

```sql
CREATE DATABASE job_dekho CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### File Upload Limits

Edit in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

## 📊 API Endpoints

### Admin Stats API
```
GET /admin/api/stats
Returns: JSON with real-time statistics
```

Response:
```json
{
  "total_students": 50,
  "total_companies": 20,
  "total_jobs": 75,
  "total_applications": 230,
  "active_jobs": 65,
  "pending_applications": 120,
  "timestamp": "2024-11-09T13:16:40.123456"
}
```

## 🚦 Usage Guide

### For Students

1. **Register** with academic details (CGPA, branch, skills)
2. **Complete Profile** and upload resume
3. **Browse Jobs** - see match scores for each job
4. **Apply** to jobs that interest you
5. **Track Status** in real-time on your dashboard

### For Companies

1. **Register** with company information
2. **Post Jobs** with detailed requirements
3. **Review Applications** sorted by match score
4. **Update Status** as you review candidates
5. **Track Hiring** metrics on your dashboard

### For Admins

1. **Login** with admin credentials
2. **Monitor Platform** via comprehensive dashboard
3. **Manage Users** - activate/deactivate accounts
4. **View Analytics** - success rates, trends, insights
5. **Oversee Jobs** and applications

## 🔒 Security Features

- Password hashing with Werkzeug
- SQL injection protection via SQLAlchemy ORM
- CSRF protection with Flask
- Secure file upload validation
- Session management with Flask-Login
- Role-based access control

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

### Database Connection Error
```bash
# Reset database
python init_db.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Template Not Found
Ensure all templates are in the `templates/` directory with correct structure.

## 📈 Future Enhancements

- [ ] Email notifications for status updates
- [ ] Resume parsing with NLP
- [ ] Video interview scheduling
- [ ] Chat system between students and companies
- [ ] Advanced analytics with charts
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Integration with LinkedIn

## 🤝 Contributing

This is a complete, ready-to-use project. Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Fork for your own use

## 📝 License

This project is for educational and commercial use.

## 👨‍💻 Support

For issues or questions:
- Check the troubleshooting section
- Review the code comments
- Test with provided sample accounts

## 🎉 Credits

Built with:
- Flask (Python web framework)
- Bootstrap 5 (Frontend framework)
- Font Awesome (Icons)
- SQLAlchemy (ORM)
- MySQL/SQLite (Database)

---

**Made with ❤️ for connecting students with their dream jobs**

© 2024 JOB DEKHO - All Rights Reserved
