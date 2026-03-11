# 📄 Resume-Based Job Viewing System

## 🎯 What Changed?

Jobs are now **ONLY visible** after a student uploads their resume. This ensures:
- Students provide their information before browsing
- Matching algorithm has data to work with
- More serious and qualified applications

---

## 🔒 How It Works

### **1. New Student Login**
```
Student Registers → Logs In → Redirected to Profile Page
                                      ↓
                        ⚠️ WARNING: "Resume Required to view jobs"
                                      ↓
                        Student uploads resume (PDF/DOCX)
                                      ↓
                        ✅ Jobs unlocked! Can now browse and apply
```

### **2. Existing Student (No Resume)**
```
Student Logs In → Tries to view Dashboard/Browse Jobs
                              ↓
                  ⚠️ Redirected to Profile Page
                              ↓
                  Flash Message: "Please upload resume first"
                              ↓
                  Student uploads resume
                              ↓
                  ✅ Can now access jobs
```

### **3. Student with Resume**
```
Student Logs In → Dashboard shows recommended jobs
                         ↓
                  Can browse all jobs
                         ↓
                  Can apply to jobs
                         ↓
                  ✅ Full access!
```

---

## 🚫 Restricted Actions Without Resume

| Action | Status | Message |
|--------|--------|---------|
| **View Dashboard** | ❌ Blocked | "Please upload your resume to view job recommendations" |
| **Browse Jobs** | ❌ Blocked | "Please upload your resume first to browse jobs" |
| **Apply to Jobs** | ❌ Blocked | "Please upload your resume before applying" |
| **View Profile** | ✅ Allowed | Can edit and upload resume |
| **My Applications** | ✅ Allowed | Can view past applications |

---

## 💡 User Experience Flow

### **Profile Page Indicators:**

#### **Without Resume:**
```
┌─────────────────────────────────────────────┐
│ ⚠️ Resume Required!                         │
│ You must upload your resume to view jobs.  │
└─────────────────────────────────────────────┘

Upload Resume (PDF/DOCX) [Required Badge]
[ Choose File ]
⚠️ Upload your resume to unlock job browsing
```

#### **With Resume:**
```
Upload Resume (PDF/DOCX)
[ Choose File ]
✓ Current: student_12345_resume.pdf
```

---

## 🔧 Technical Implementation

### **Backend Checks (student.py):**

```python
# Dashboard Route
@student_bp.route('/dashboard')
def dashboard():
    student = current_user.student
    
    # NEW: Check if resume uploaded
    if not student.resume_path:
        flash('Please upload your resume to view job recommendations', 'warning')
        return redirect(url_for('student.profile'))
    
    # Continue with normal dashboard logic...
```

```python
# Browse Jobs Route
@student_bp.route('/browse-jobs')
def browse_jobs():
    student = current_user.student
    
    # NEW: Check if resume uploaded - REQUIRED
    if not student.resume_path:
        flash('Please upload your resume first to browse jobs', 'warning')
        return redirect(url_for('student.profile'))
    
    # Show jobs only if resume exists...
```

```python
# Apply for Job Route
@student_bp.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    student = current_user.student
    
    # NEW: Check if resume uploaded
    if not student.resume_path:
        flash('Please upload your resume before applying', 'danger')
        return redirect(url_for('student.profile'))
    
    # Process application...
```

### **Frontend Indicators (profile.html):**

```html
<!-- Warning Alert -->
{% if not student.resume_path %}
<div class="alert alert-warning">
    <i class="fas fa-exclamation-triangle"></i>
    <strong>Resume Required!</strong> You must upload your resume to view and apply for jobs.
</div>
{% endif %}

<!-- Required Badge on Input -->
<label>
    Upload Resume (PDF/DOCX) 
    {% if not student.resume_path %}
    <span class="badge bg-danger">Required</span>
    {% endif %}
</label>

<!-- Make field required if no resume -->
<input type="file" name="resume" 
       {% if not student.resume_path %}required{% endif %}>
```

---

## 📊 Database Check

The system checks: `student.resume_path` field in database

- **NULL or Empty** → Jobs blocked
- **Has filename** → Jobs accessible

```sql
-- Check student resume status
SELECT name, roll_number, resume_path,
       CASE 
           WHEN resume_path IS NULL THEN 'No Access'
           WHEN resume_path = '' THEN 'No Access'
           ELSE 'Full Access'
       END as job_access_status
FROM students;
```

---

## 🎨 Visual Indicators

### **Navigation Menu:**
```
Student Dashboard
├── 🏠 Dashboard         → Requires resume
├── 💼 Browse Jobs       → Requires resume  
├── 📋 My Applications   → Always accessible
└── 👤 Profile           → Always accessible
```

### **Profile Page States:**

**State 1: No Resume**
```
┌─────────────────────────────────────┐
│ ⚠️ Resume Required!                 │
│                                     │
│ [Upload Resume] ← Required Badge    │
│ ⚠️ Upload to unlock job browsing    │
│                                     │
│ [Save Changes] ← Button enabled     │
└─────────────────────────────────────┘
```

**State 2: Resume Uploaded**
```
┌─────────────────────────────────────┐
│ [Upload Resume]                     │
│ ✓ Current: resume.pdf               │
│                                     │
│ [Save Changes]                      │
└─────────────────────────────────────┘
```

---

## 🔄 Sample User Journey

### **Rahul's First Login:**

1. **Registers:** Creates account with email/password
2. **Logs in:** Redirected to dashboard
3. **Blocked:** Sees warning, redirected to profile
4. **Uploads:** Submits resume PDF (2MB)
5. **Success:** Can now browse 25 matching jobs
6. **Applies:** One-click apply to Google SDE role
7. **Tracks:** Views application status in real-time

### **Timeline:**
```
09:00 AM - Registration complete
09:01 AM - Login successful
09:01 AM - ⚠️ Blocked from dashboard
09:02 AM - Redirected to profile
09:05 AM - Resume uploaded successfully
09:05 AM - ✅ Jobs unlocked!
09:06 AM - Browsing 25 matched jobs
09:07 AM - Applied to Google SDE
09:07 AM - Status: Applied (Match: 92%)
```

---

## 🛡️ Security & Validation

### **File Upload Restrictions:**
- **Allowed formats:** PDF, DOC, DOCX
- **Max size:** 16 MB
- **Filename:** Sanitized (removes special chars)
- **Storage:** `uploads/resumes/` directory
- **Naming:** `{roll_number}_{original_name}.pdf`

### **Access Control:**
```python
# Triple-layer protection
1. @login_required         # Must be logged in
2. @student_required       # Must be student role
3. if not student.resume_path:  # Must have resume
```

---

## 📈 Benefits

### **For Students:**
✅ Guided onboarding process
✅ Clear requirements before job browsing
✅ Better matches based on resume data
✅ Professional application process

### **For Companies:**
✅ All applicants have resumes
✅ Better quality applications
✅ Complete candidate profiles
✅ Reduced spam applications

### **For System:**
✅ Complete data for matching algorithm
✅ Higher engagement (resume = serious intent)
✅ Better analytics and reporting
✅ Professional platform reputation

---

## 🧪 Testing the Feature

### **Test Case 1: New Student**
```bash
1. Register new student
2. Login
3. Try to access /student/dashboard
4. Expected: Redirected to /student/profile
5. Expected: Warning message shown
6. Upload resume
7. Try to access /student/dashboard again
8. Expected: Dashboard loads successfully
```

### **Test Case 2: Existing Student (No Resume)**
```bash
1. Login as student without resume
2. Try to access /student/browse-jobs
3. Expected: Redirected to /student/profile
4. Expected: "Please upload your resume first" message
```

### **Test Case 3: Apply Without Resume**
```bash
1. Login as student without resume
2. Try to POST /student/apply/1
3. Expected: Redirected to /student/profile
4. Expected: "Please upload your resume before applying" error
```

---

## 📝 Summary

**Before:** Students could browse and apply to jobs without providing resume
**After:** Resume upload is **MANDATORY** before accessing any job-related features

This ensures:
- 🎯 Better quality applications
- 📊 Complete data for matching
- 💼 Professional candidate experience
- 🔒 Serious applicants only

---

## 🚀 Quick Reference

**Resume uploaded?**
- ✅ YES → Full access to jobs, applications, dashboard
- ❌ NO → Only profile and past applications accessible

**Where to upload?**
- Student → Profile → Upload Resume section

**What happens after upload?**
- Instant access to all jobs
- Matching algorithm calculates scores
- Can apply to jobs immediately

---

**Status:** ✅ Implemented and Active
**Version:** 2.0
**Date:** Current
