# Job Dekho - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1️⃣ Install Dependencies
```bash
pip install -r requirements_complete.txt
```

### 2️⃣ Run the Application
```bash
python start.py
```

### 3️⃣ Choose Your Version
- **Option 1:** Flask Web App → http://127.0.0.1:5000
- **Option 2:** Streamlit with TTS → http://localhost:8501
- **Option 3:** Demo Mode (console)

---

## 📌 Quick Commands

### Run Flask Directly
```bash
python app.py
```

### Run Streamlit Directly
```bash
streamlit run streamlit_app.py
```

### Run Demo
```bash
python demo_job_dekho.py
```

### Clean Up Project
```bash
python cleanup.py
```

---

## 👥 Test Accounts

### Create Your Own Accounts
**For Students:**
1. Go to Register page
2. Choose "Student" role
3. Fill in: name, roll number, CGPA, branch, skills
4. Upload resume (optional)

**For Companies:**
1. Go to Register page
2. Choose "Company" role
3. Fill in: company name, industry, description
4. Post jobs from dashboard

---

## 🎯 Key Features

### Smart Matching Algorithm
- **70%+ match** = Excellent (🟢)
- **50-69% match** = Good (🟡)
- **<50% match** = Partial (🔵)

### Auto-Shortlisting
Students with **100% match** (all criteria met) are automatically shortlisted!

### Matching Criteria
- **CGPA (40%)** - Must meet minimum requirement
- **Branch (30%)** - Must match or be "Any"
- **Skills (30%)** - At least one skill must match

---

## 🔊 Text-to-Speech (Streamlit Only)

### How to Use TTS
1. Click 🔊 button next to any text
2. Use sidebar controls to stop/pause
3. Test TTS in sidebar with custom text

### TTS Features
- ✅ Page navigation announcements
- ✅ Job description narration
- ✅ Candidate information reading
- ✅ Success/error notifications
- ✅ Custom test input

---

## ❓ Common Issues

### "Module not found"
```bash
pip install -r requirements_complete.txt
```

### Port already in use
Flask: Change port in `app.py`
Streamlit: `streamlit run streamlit_app.py --server.port 8502`

### TTS not working
Windows only! Test: `python -c "import pyttsx3; e=pyttsx3.init(); e.say('Test'); e.runAndWait()"`

### Database error
Delete database file and restart:
- Flask: `instance\job_dekho.db`
- Streamlit: `job_dekho_streamlit.db`

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `start.py` | Main launcher |
| `app.py` | Flask application |
| `streamlit_app.py` | Streamlit app |
| `demo_job_dekho.py` | Console demo |
| `requirements_complete.txt` | Dependencies |
| `cleanup.py` | Remove unused files |
| `SETUP_GUIDE.md` | Full setup guide |

---

## 📊 Workflow

### Student Workflow
1. Register → 2. Upload Resume → 3. Browse Jobs → 4. Apply → 5. Track Status

### Company Workflow
1. Register → 2. Post Job → 3. View Applications → 4. Update Status → 5. Hire

---

## 🎓 Sample Data

### Sample Student Profile
- **Name:** John Doe
- **Roll:** CS2021001
- **CGPA:** 8.5
- **Branch:** Computer Science
- **Skills:** Python, Java, React, SQL

### Sample Job Post
- **Title:** Software Developer
- **Min CGPA:** 7.0
- **Branch:** Computer Science
- **Skills:** Python, React
- **Salary:** 6-8 LPA
- **Location:** Bangalore

---

## 💡 Pro Tips

1. **Use Streamlit for better UX** - Modern UI with TTS
2. **Enable TTS for accessibility** - Voice-guided navigation
3. **Match score helps prioritization** - Focus on high-match jobs
4. **Auto-shortlisting saves time** - Qualified candidates auto-flagged
5. **Update skills regularly** - Better matching results

---

## 🆘 Need Help?

1. **Full Guide:** Read `SETUP_GUIDE.md`
2. **Features:** Check `README.md`
3. **Demo:** Run `python demo_job_dekho.py`
4. **Test:** Try both Flask and Streamlit versions

---

**🏢 Job Dekho - Smart Job Matching Made Easy!**

*For detailed information, see SETUP_GUIDE.md*
