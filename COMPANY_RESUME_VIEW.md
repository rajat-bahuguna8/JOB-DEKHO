# 👔 Company Resume Viewing Feature

## 🎯 Overview

Companies can now **view and download student resumes** directly from the application management interface. This feature allows recruiters to review candidate profiles thoroughly before making hiring decisions.

---

## ✨ Key Features

### 1. **View Resume Button**
- Available on application cards
- Opens resume in new browser tab
- Supports PDF viewing in browser

### 2. **Security & Access Control**
- ✅ Only authenticated companies can access
- ✅ Can only view resumes of students who applied to their jobs
- ✅ Cannot access resumes of students who didn't apply
- ✅ Requires student to have uploaded resume

### 3. **Multiple Access Points**
Companies can view resumes from:
- 📊 **Company Dashboard** - Recent applications section
- 📋 **Job Applications Page** - Full applicant details
- 🔍 Direct link per candidate

---

## 🖥️ User Interface

### **Job Applications Page:**
```
┌─────────────────────────────────────────────────────┐
│ Rahul Sharma                                        │
│ Roll Number: CS2021001                              │
│ CGPA: 8.5 | Branch: Computer Science                │
│ Skills: Python, Java, React, Node.js                │
│ Phone: +91-9876543210 | Email: rahul@student.com   │
│ Applied: 11 Nov 2025, 02:30 PM                      │
│                                                      │
│ [📄 View Resume] ← Click to open PDF               │
└─────────────────────────────────────────────────────┘
```

### **Company Dashboard:**
```
Recent Applications
┌─────────────────────────────────────────────┐
│ Rahul Sharma - Software Developer    [📄]  │
│ Applied | Match: 92%                        │
└─────────────────────────────────────────────┘
```

---

## 🔄 How It Works

### **Scenario 1: View Resume from Applications Page**

```
1. Company logs in
2. Goes to "My Jobs"
3. Clicks on a job posting
4. Sees list of applicants with details
5. Clicks "View Resume" button
6. Resume opens in new tab (PDF viewer)
7. Can download, print, or close
```

### **Scenario 2: Quick View from Dashboard**

```
1. Company logs in → Dashboard
2. Sees "Recent Applications" section
3. Clicks PDF icon next to applicant name
4. Resume opens instantly in new tab
```

### **Scenario 3: Access Denied (Security)**

```
1. Company tries to view resume of student who didn't apply
2. System checks: Did student apply to this company's job?
3. Result: NO
4. Shows error: "Access denied - student did not apply"
5. Redirects back
```

---

## 🔐 Security Implementation

### **Three-Layer Access Control:**

```python
# Layer 1: Must be logged in
@login_required

# Layer 2: Must be a company
@company_required

# Layer 3: Must have received application
def view_resume(student_id):
    # Check if student applied to company's job
    has_applied = False
    for job in company.jobs:
        for app in job.applications:
            if app.student_id == student_id:
                has_applied = True
                
    if not has_applied:
        return "Access Denied"
```

### **What Companies Can/Cannot Do:**

| Action | Allowed? | Reason |
|--------|----------|--------|
| View resume of applicant | ✅ YES | Student applied to their job |
| View resume of non-applicant | ❌ NO | No business relationship |
| Download resume | ✅ YES | For hiring process |
| Share resume URL | ❌ NO | URL requires authentication |
| View resume after rejection | ✅ YES | Historical record |

---

## 📊 Application Details Shown

When viewing applications, companies see:

### **Student Information:**
- ✅ Full Name
- ✅ Roll Number
- ✅ CGPA
- ✅ Branch/Major
- ✅ Skills (comma-separated)
- ✅ Phone Number
- ✅ Email Address
- ✅ Application Date & Time
- ✅ Resume (if uploaded)

### **Application Metadata:**
- Match Score (percentage)
- Current Status
- Applied Date/Time
- Job Title

---

## 🎨 Visual Design

### **View Resume Button States:**

#### **Resume Available:**
```html
[📄 View Resume]  ← Green button, clickable
Status: btn-success
Icon: fa-file-pdf
Action: Opens resume in new tab
```

#### **No Resume:**
```html
⚠️ No resume uploaded  ← Gray text, not clickable
Status: text-muted
Icon: fa-exclamation-circle
Action: None
```

### **Button Variations:**

**Full Button (Applications Page):**
```
┌───────────────────┐
│ 📄 View Resume    │
└───────────────────┘
Color: Green (#28a745)
Size: Small (btn-sm)
```

**Icon Only (Dashboard):**
```
┌────┐
│ 📄 │
└────┘
Color: Green Outline
Size: Small
Tooltip: "View Resume"
```

---

## 🔧 Technical Implementation

### **Backend Route (company.py):**

```python
@company_bp.route('/view-resume/<int:student_id>')
@login_required
@company_required
def view_resume(student_id):
    """View/download student resume - only if student applied"""
    student = Student.query.get_or_404(student_id)
    company = current_user.company
    
    # Security check: Has student applied to company's job?
    has_applied = False
    for job in company.jobs:
        for app in job.applications:
            if app.student_id == student_id:
                has_applied = True
                break
        if has_applied:
            break
    
    if not has_applied:
        flash('You can only view resumes of students who applied', 'danger')
        return redirect(url_for('company.dashboard'))
    
    if not student.resume_path:
        flash('Student has not uploaded a resume', 'warning')
        return redirect(request.referrer)
    
    # Send the PDF file
    resume_directory = os.path.join(os.getcwd(), 'uploads', 'resumes')
    return send_from_directory(resume_directory, student.resume_path)
```

### **Frontend Template (job_applications.html):**

```html
<!-- View Resume Button -->
{% if app.student.resume_path %}
<a href="{{ url_for('company.view_resume', student_id=app.student.id) }}" 
   class="btn btn-sm btn-success" 
   target="_blank">
    <i class="fas fa-file-pdf"></i> View Resume
</a>
{% else %}
<span class="text-muted">
    <i class="fas fa-exclamation-circle"></i> No resume uploaded
</span>
{% endif %}
```

---

## 📁 File Handling

### **Resume Storage:**
- **Location:** `uploads/resumes/`
- **Naming:** `{roll_number}_{original_filename}.pdf`
- **Format:** PDF, DOC, DOCX (16MB max)

### **Example Resume Path:**
```
uploads/resumes/CS2021001_Rahul_Resume.pdf
```

### **URL Structure:**
```
http://localhost:5000/company/view-resume/5
                                         ↑
                                    Student ID
```

---

## 🚀 Usage Scenarios

### **Scenario A: Initial Screening**

```
TechCorp HR Manager:
1. Posts "Python Developer" job
2. Receives 50 applications
3. Sorts by match score (highest first)
4. Reviews top 10 candidates:
   - Checks CGPA, skills, branch
   - Clicks "View Resume" for each
   - Opens 10 tabs with resumes
5. Compares side-by-side
6. Shortlists 5 best candidates
7. Updates status to "Shortlisted"
```

### **Scenario B: Interview Preparation**

```
Company Interviewer:
1. Dashboard shows 3 interview-scheduled applicants
2. Clicks PDF icon next to each name
3. Opens all 3 resumes in separate tabs
4. Reviews projects, experience, education
5. Prepares technical questions
6. Conducts interviews
```

### **Scenario C: Final Decision**

```
Hiring Manager:
1. Goes to "Software Engineer" job applications
2. Filters: Status = "Interview"
3. Sees 2 candidates with 95% and 92% match
4. Views both resumes
5. Compares:
   - Projects done
   - Internship experience
   - Certifications
6. Selects best candidate
7. Updates status to "Selected"
```

---

## ✅ Benefits

### **For Companies:**
- 📄 Easy access to candidate resumes
- 🔒 Secure, permission-based viewing
- ⚡ Fast review process (opens in new tab)
- 📊 All info in one place (resume + profile)
- 💾 Can download for records

### **For Students:**
- 🎯 Resume reaches recruiters directly
- 🔐 Privacy protected (only applied companies)
- ✨ Professional presentation
- 📈 Higher chances of review

### **For System:**
- 🛡️ Secure file serving
- 📁 Organized storage
- 🔍 Easy tracking
- 💼 Professional workflow

---

## 🧪 Testing the Feature

### **Test Case 1: Successful Resume View**
```bash
1. Login as company (hr@techcorp.com)
2. Go to Dashboard
3. See recent application: "Rahul Sharma - SDE"
4. Click PDF icon
5. Expected: Resume opens in new tab
6. Expected: PDF displays correctly
```

### **Test Case 2: No Resume Uploaded**
```bash
1. Login as company
2. Go to job applications
3. See applicant without resume
4. Expected: "No resume uploaded" message shown
5. Expected: No "View Resume" button
```

### **Test Case 3: Unauthorized Access**
```bash
1. Login as Company A
2. Try to access: /company/view-resume/999
   (Student 999 didn't apply to Company A)
3. Expected: "Access denied" message
4. Expected: Redirect to dashboard
```

### **Test Case 4: Direct URL Access**
```bash
1. Logout (no authentication)
2. Try: http://localhost:5000/company/view-resume/5
3. Expected: Redirect to login page
4. Expected: "Please log in" message
```

---

## 🔄 User Flow Diagram

```
Company Dashboard
       ↓
[View Applications]
       ↓
Application List (sorted by match score)
       ↓
┌─────────────────────────────────┐
│ Candidate Details               │
│ - Name, Roll, CGPA              │
│ - Skills, Branch                │
│ - Phone, Email                  │
│ - Match Score: 92%              │
│                                 │
│ [📄 View Resume] ← Click        │
└─────────────────────────────────┘
       ↓
Security Check: Has Applied?
       ↓
    YES → Open Resume PDF
       ↓
New Tab Opens
       ↓
PDF Viewer shows resume
       ↓
Company reviews content
       ↓
[Download] or [Print] or [Close]
       ↓
Return to applications page
       ↓
Update application status
```

---

## 📝 Sample Application Card

```
┌──────────────────────────────────────────────────────────┐
│                     RAHUL SHARMA                         │
│ ──────────────────────────────────────────────────────── │
│ Roll Number: CS2021001                                   │
│ CGPA: 8.5 | Branch: Computer Science                    │
│ Skills: Python, Java, React, Node.js, MongoDB           │
│ Phone: +91-9876543210 | Email: rahul@student.com        │
│ Applied: 11 Nov 2025, 02:30 PM                          │
│                                                          │
│ [📄 View Resume] ← Green Button                         │
│                                                          │
│ Match Score: ████████████████░░░░ 92%                   │
│ Status: [Applied ▼] [Update]                            │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Quick Reference

### **Where to Find Resume View:**

1. **Company Dashboard**
   - Path: `/company/dashboard`
   - Location: Recent Applications section
   - Display: PDF icon button

2. **Job Applications Page**
   - Path: `/company/job/<id>/applications`
   - Location: Each applicant card
   - Display: Full "View Resume" button

### **Button Behavior:**
- **Click:** Opens resume in new browser tab
- **Target:** `target="_blank"` (new tab)
- **Format:** PDF viewed in browser
- **Actions:** View, Download, Print

### **Access Requirements:**
- ✅ Must be logged in
- ✅ Must be company role
- ✅ Student must have applied
- ✅ Resume must exist

---

## 🚀 Status

**Implementation:** ✅ Complete
**Testing:** ✅ Ready
**Security:** ✅ Implemented
**Documentation:** ✅ Complete

---

**Enjoy hassle-free candidate review! 🎉**
