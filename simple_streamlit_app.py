"""
Job Dekho - Simple Streamlit Application (No PyArrow)
A working version without problematic dependencies
"""

import streamlit as st
import sys
import os
from datetime import datetime
import sqlite3
import hashlib

# Simple configuration
st.set_page_config(
    page_title="Job Dekho - Smart Job Portal with TTS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Simple TTS function
def simple_tts(text):
    """Simple TTS using Windows SAPI"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return True
    except:
        return False

def create_tts_button(text, key=None, help_text="Click to hear this text"):
    """Create a simple TTS button"""
    if st.button("🔊 Listen", key=key, help=help_text):
        if simple_tts(text):
            st.success("🎵 Playing audio...")
        else:
            st.warning("TTS not available")

# Simple database functions
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('job_dekho_simple.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            cgpa REAL NOT NULL,
            branch TEXT NOT NULL,
            skills TEXT,
            phone TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create companies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT NOT NULL,
            industry TEXT,
            description TEXT,
            website TEXT,
            contact_person TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            min_cgpa REAL NOT NULL,
            required_branch TEXT NOT NULL,
            required_skills TEXT,
            salary TEXT,
            location TEXT,
            job_type TEXT DEFAULT 'Full-time',
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies (id)
        )
    ''')
    
    # Create applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            job_id INTEGER,
            status TEXT DEFAULT 'Applied',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (job_id) REFERENCES jobs (id),
            UNIQUE(student_id, job_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_value):
    """Verify password against hash"""
    return hashlib.sha256(password.encode()).hexdigest() == hash_value

def authenticate_user(email, password):
    """Authenticate user"""
    conn = sqlite3.connect('job_dekho_simple.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, email, password_hash, role FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user[2]):
        return {'id': user[0], 'email': user[1], 'role': user[3]}
    return None

def register_user(user_data):
    """Register new user"""
    conn = sqlite3.connect('job_dekho_simple.db')
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (user_data['email'],))
        if cursor.fetchone():
            return False, "Email already registered!"
        
        # Create user
        password_hash = hash_password(user_data['password'])
        cursor.execute(
            'INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)',
            (user_data['email'], password_hash, user_data['role'])
        )
        user_id = cursor.lastrowid
        
        # Create profile based on role
        if user_data['role'] == 'student':
            cursor.execute('''
                INSERT INTO students (user_id, name, roll_number, cgpa, branch, skills, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, user_data['name'], user_data['roll_number'],
                user_data['cgpa'], user_data['branch'], 
                user_data.get('skills', ''), user_data.get('phone', '')
            ))
        elif user_data['role'] == 'company':
            cursor.execute('''
                INSERT INTO companies (user_id, name, industry, description, website, contact_person)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id, user_data['name'], user_data.get('industry', ''),
                user_data.get('description', ''), user_data.get('website', ''),
                user_data.get('contact_person', '')
            ))
        
        conn.commit()
        return True, "Registration successful!"
        
    except Exception as e:
        conn.rollback()
        return False, f"Registration failed: {str(e)}"
    finally:
        conn.close()

def calculate_match_score(student_cgpa, student_branch, student_skills, job_cgpa, job_branch, job_skills):
    """Simple matching algorithm"""
    score = 0
    
    # CGPA match (40 points)
    if student_cgpa >= job_cgpa:
        score += min((student_cgpa / 10.0) * 40, 40)
    
    # Branch match (30 points)
    if student_branch == job_branch or job_branch == "Any":
        score += 30
    
    # Skills match (30 points)
    if student_skills and job_skills:
        student_skill_list = [s.strip().lower() for s in student_skills.split(',')]
        job_skill_list = [s.strip().lower() for s in job_skills.split(',')]
        
        matching_skills = set(student_skill_list) & set(job_skill_list)
        if matching_skills and job_skill_list:
            score += (len(matching_skills) / len(job_skill_list)) * 30
    
    return round(score, 1)

# Initialize database
init_database()

def show_sidebar():
    """Show sidebar"""
    with st.sidebar:
        st.title("🏢 Job Dekho")
        
        if st.session_state.user_id:
            st.success(f"✅ Logged in as {st.session_state.user_role}")
            st.caption(f"📧 {st.session_state.user_email}")
            
            st.markdown("---")
            st.subheader("📱 Navigation")
            
            if st.session_state.user_role == 'student':
                if st.button("🎓 Student Dashboard", key="nav_student"):
                    st.session_state.page = 'student_dashboard'
                    st.rerun()
            elif st.session_state.user_role == 'company':
                if st.button("🏢 Company Dashboard", key="nav_company"):
                    st.session_state.page = 'company_dashboard'
                    st.rerun()
                if st.button("➕ Post Job", key="nav_post_job"):
                    st.session_state.page = 'post_job'
                    st.rerun()
            
            if st.button("🏠 Home", key="nav_home"):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("🚪 Logout", key="nav_logout"):
                st.session_state.user_id = None
                st.session_state.user_role = None
                st.session_state.user_email = None
                st.session_state.page = 'home'
                st.success("Logged out successfully!")
                st.rerun()
        else:
            st.info("Not logged in")
            if st.button("🔐 Login", key="nav_login"):
                st.session_state.page = 'login'
                st.rerun()
            if st.button("📝 Register", key="nav_register"):
                st.session_state.page = 'register'
                st.rerun()
        
        # TTS Test
        st.markdown("---")
        st.subheader("🔊 TTS Test")
        test_text = st.text_input("Test TTS:", value="Hello! This is Job Dekho!")
        if st.button("🔊 Test Speak", key="test_tts"):
            if simple_tts(test_text):
                st.success("TTS Working! 🎵")
            else:
                st.error("TTS Not Available ❌")

def show_home():
    """Home page"""
    if simple_tts("Welcome to Job Dekho"):
        pass  # TTS announcement
    
    st.title("🏢 Job Dekho - Smart Job Portal")
    st.markdown("### Your intelligent job matching platform with voice assistance")
    
    page_desc = "Welcome to Job Dekho! An intelligent platform connecting students with companies through smart matching algorithms and voice assistance."
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(page_desc)
    with col2:
        create_tts_button(page_desc, key="home_desc")
    
    if not st.session_state.user_id:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎓 For Students")
            st.markdown("""
            - Find jobs matching your skills
            - Get automatically shortlisted
            - Track application status
            - Voice-guided interface
            """)
            if st.button("Register as Student", key="reg_student"):
                st.session_state.page = 'register'
                st.rerun()
        
        with col2:
            st.subheader("🏢 For Companies")
            st.markdown("""
            - Post job requirements
            - Get matched candidates
            - Manage applications
            - Analytics dashboard
            """)
            if st.button("Register as Company", key="reg_company"):
                st.session_state.page = 'register'
                st.rerun()
        
        st.markdown("**Already have an account?**")
        if st.button("Login Here", key="goto_login"):
            st.session_state.page = 'login'
            st.rerun()
    else:
        st.success(f"Welcome back, {st.session_state.user_email}!")
        if st.session_state.user_role == 'student':
            if st.button("Go to Dashboard", key="goto_dash"):
                st.session_state.page = 'student_dashboard'
                st.rerun()
        elif st.session_state.user_role == 'company':
            if st.button("Go to Dashboard", key="goto_dash"):
                st.session_state.page = 'company_dashboard'
                st.rerun()

def show_login():
    """Login page"""
    st.title("🔐 Login to Job Dekho")
    
    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if email and password:
                user = authenticate_user(email, password)
                if user:
                    st.session_state.user_id = user['id']
                    st.session_state.user_role = user['role']
                    st.session_state.user_email = user['email']
                    
                    success_msg = f"Welcome back! Logged in as {user['role']}"
                    st.success(success_msg)
                    simple_tts(success_msg)
                    
                    if user['role'] == 'student':
                        st.session_state.page = 'student_dashboard'
                    else:
                        st.session_state.page = 'company_dashboard'
                    st.rerun()
                else:
                    error_msg = "Invalid email or password!"
                    st.error(error_msg)
                    simple_tts(error_msg)
            else:
                st.warning("Please enter both email and password")
    
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

def show_register():
    """Registration page"""
    st.title("📝 Register for Job Dekho")
    
    with st.form("register_form"):
        st.subheader("Basic Information")
        email = st.text_input("Email Address*")
        password = st.text_input("Password*", type="password")
        role = st.selectbox("I am a:", ["", "student", "company"])
        
        name = None
        if role == "student":
            st.subheader("Student Information")
            name = st.text_input("Full Name*")
            roll_number = st.text_input("Roll Number*")
            cgpa = st.number_input("CGPA*", min_value=0.0, max_value=10.0, step=0.01)
            branch = st.selectbox("Branch*", [
                "", "Computer Science", "Information Technology", "Electronics", 
                "Mechanical", "Civil", "Electrical", "Other"
            ])
            skills = st.text_area("Skills (comma separated)*", placeholder="e.g., Python, Java, React")
            phone = st.text_input("Phone Number")
            
        elif role == "company":
            st.subheader("Company Information")
            name = st.text_input("Company Name*")
            industry = st.text_input("Industry")
            description = st.text_area("Company Description")
            website = st.text_input("Website")
            contact_person = st.text_input("Contact Person")
        
        submit = st.form_submit_button("Register")
        
        if submit:
            if not email or not password or not role or not name:
                st.warning("Please fill in all required fields marked with *")
                return
            
            user_data = {
                'email': email,
                'password': password,
                'role': role,
                'name': name
            }
            
            if role == "student":
                if not all([roll_number, cgpa, branch, skills]):
                    st.warning("Please fill in all required student information")
                    return
                user_data.update({
                    'roll_number': roll_number,
                    'cgpa': cgpa,
                    'branch': branch,
                    'skills': skills,
                    'phone': phone
                })
            elif role == "company":
                user_data.update({
                    'industry': industry,
                    'description': description,
                    'website': website,
                    'contact_person': contact_person
                })
            
            success, message = register_user(user_data)
            if success:
                st.success(message)
                simple_tts(message)
                st.info("Please login with your new account.")
            else:
                st.error(message)
                simple_tts(message)
    
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

def show_student_dashboard():
    """Student dashboard"""
    if not st.session_state.user_id or st.session_state.user_role != 'student':
        st.error("Access denied. Please login as a student.")
        return
    
    st.title("🎓 Student Dashboard")
    
    # Get student data
    conn = sqlite3.connect('job_dekho_simple.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, roll_number, cgpa, branch, skills, phone 
        FROM students WHERE user_id = ?
    ''', (st.session_state.user_id,))
    student = cursor.fetchone()
    
    if not student:
        st.error("Student profile not found.")
        return
    
    name, roll_number, cgpa, branch, skills, phone = student
    
    welcome_msg = f"Welcome back, {name}!"
    st.subheader(welcome_msg)
    create_tts_button(welcome_msg, key="welcome")
    
    # Profile summary
    with st.expander("📋 Your Profile", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CGPA", cgpa)
        with col2:
            st.metric("Branch", branch)
        with col3:
            st.metric("Roll Number", roll_number)
        
        if skills:
            st.write(f"**Skills:** {skills}")
        if phone:
            st.write(f"**Phone:** {phone}")
    
    # Get applications and jobs
    cursor.execute('''
        SELECT COUNT(*) FROM applications 
        WHERE student_id = (SELECT id FROM students WHERE user_id = ?)
    ''', (st.session_state.user_id,))
    total_applications = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM applications a
        JOIN students s ON a.student_id = s.id
        WHERE s.user_id = ? AND a.status = 'Shortlisted'
    ''', (st.session_state.user_id,))
    shortlisted = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE is_active = 1')
    total_jobs = cursor.fetchone()[0]
    
    # Statistics
    st.subheader("📊 Your Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Applications", total_applications)
    with col2:
        st.metric("Shortlisted", shortlisted)
    with col3:
        st.metric("Available Jobs", total_jobs)
    
    # Available Jobs
    st.subheader("💼 Available Jobs")
    cursor.execute('''
        SELECT j.id, j.title, j.description, j.min_cgpa, j.required_branch, 
               j.required_skills, j.salary, j.location, c.name as company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        WHERE j.is_active = 1
        ORDER BY j.created_at DESC
    ''')
    jobs = cursor.fetchall()
    
    if jobs:
        for job in jobs:
            job_id, title, description, min_cgpa, req_branch, req_skills, salary, location, company_name = job
            
            # Check if already applied
            cursor.execute('''
                SELECT status FROM applications a
                JOIN students s ON a.student_id = s.id
                WHERE s.user_id = ? AND a.job_id = ?
            ''', (st.session_state.user_id, job_id))
            application = cursor.fetchone()
            
            with st.expander(f"🏢 {title} at {company_name}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Description:** {description}")
                    st.write(f"**Required CGPA:** {min_cgpa}+")
                    st.write(f"**Branch:** {req_branch}")
                    st.write(f"**Skills:** {req_skills}")
                    if salary:
                        st.write(f"**Salary:** {salary}")
                    if location:
                        st.write(f"**Location:** {location}")
                    
                    # Calculate match score
                    score = calculate_match_score(cgpa, branch, skills, min_cgpa, req_branch, req_skills)
                    if score >= 70:
                        st.success(f"🎯 Excellent Match: {score}% compatibility")
                    elif score >= 50:
                        st.warning(f"⚠️ Good Match: {score}% compatibility")
                    else:
                        st.info(f"ℹ️ Partial Match: {score}% compatibility")
                
                with col2:
                    # TTS button
                    job_text = f"""
                    Job: {title} at {company_name}
                    Description: {description}
                    Required CGPA: {min_cgpa} or above
                    Branch: {req_branch}
                    Skills: {req_skills}
                    Compatibility: {score} percent
                    """
                    create_tts_button(job_text.strip(), key=f"job_tts_{job_id}")
                    
                    if application:
                        st.success(f"Applied ✓\n({application[0]})")
                    else:
                        if st.button(f"Apply Now", key=f"apply_{job_id}"):
                            # Apply for job
                            cursor.execute('SELECT id FROM students WHERE user_id = ?', (st.session_state.user_id,))
                            student_id = cursor.fetchone()[0]
                            
                            status = "Shortlisted" if score >= 100 else "Applied"
                            
                            cursor.execute('''
                                INSERT INTO applications (student_id, job_id, status)
                                VALUES (?, ?, ?)
                            ''', (student_id, job_id, status))
                            conn.commit()
                            
                            if status == 'Shortlisted':
                                success_msg = f"Congratulations! You've been automatically shortlisted for {title}!"
                                st.success(success_msg)
                                simple_tts(success_msg)
                            else:
                                success_msg = f"Application submitted for {title}!"
                                st.success(success_msg)
                                simple_tts(success_msg)
                            
                            st.rerun()
    else:
        st.info("No jobs available at the moment.")
    
    conn.close()

def show_company_dashboard():
    """Company dashboard"""
    if not st.session_state.user_id or st.session_state.user_role != 'company':
        st.error("Access denied. Please login as a company.")
        return
    
    st.title("🏢 Company Dashboard")
    
    conn = sqlite3.connect('job_dekho_simple.db')
    cursor = conn.cursor()
    
    # Get company data
    cursor.execute('SELECT name, industry, description FROM companies WHERE user_id = ?', 
                  (st.session_state.user_id,))
    company = cursor.fetchone()
    
    if not company:
        st.error("Company profile not found.")
        return
    
    name, industry, description = company
    
    welcome_msg = f"Welcome, {name}!"
    st.subheader(welcome_msg)
    create_tts_button(welcome_msg, key="company_welcome")
    
    # Company info
    with st.expander("🏢 Company Information", expanded=True):
        st.write(f"**Industry:** {industry or 'Not specified'}")
        if description:
            st.write(f"**Description:** {description}")
    
    # Statistics
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE company_id = (SELECT id FROM companies WHERE user_id = ?)', 
                  (st.session_state.user_id,))
    total_jobs = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM applications a
        JOIN jobs j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        WHERE c.user_id = ?
    ''', (st.session_state.user_id,))
    total_applications = cursor.fetchone()[0]
    
    st.subheader("📊 Your Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Jobs Posted", total_jobs)
    with col2:
        st.metric("Total Applications", total_applications)
    
    # Action buttons
    if st.button("➕ Post New Job", key="post_job"):
        st.session_state.page = 'post_job'
        st.rerun()
    
    # Posted Jobs
    if total_jobs > 0:
        st.subheader("📝 Your Posted Jobs")
        cursor.execute('''
            SELECT j.id, j.title, j.description, j.min_cgpa, j.required_branch,
                   j.required_skills, j.salary, j.location, j.created_at,
                   COUNT(a.id) as app_count
            FROM jobs j
            LEFT JOIN applications a ON j.id = a.job_id
            WHERE j.company_id = (SELECT id FROM companies WHERE user_id = ?)
            GROUP BY j.id
            ORDER BY j.created_at DESC
        ''', (st.session_state.user_id,))
        jobs = cursor.fetchall()
        
        for job in jobs:
            job_id, title, desc, min_cgpa, branch, skills, salary, location, created, app_count = job
            
            with st.expander(f"📋 {title} ({app_count} applications)"):
                st.write(f"**Description:** {desc}")
                st.write(f"**Required CGPA:** {min_cgpa}+")
                st.write(f"**Branch:** {branch}")
                st.write(f"**Skills:** {skills}")
                if salary:
                    st.write(f"**Salary:** {salary}")
                if location:
                    st.write(f"**Location:** {location}")
                
                # Show applications
                if app_count > 0:
                    cursor.execute('''
                        SELECT s.name, s.branch, s.cgpa, s.skills, a.status, a.id
                        FROM applications a
                        JOIN students s ON a.student_id = s.id
                        WHERE a.job_id = ?
                        ORDER BY a.applied_at DESC
                    ''', (job_id,))
                    applications = cursor.fetchall()
                    
                    st.write("**Applications:**")
                    for app in applications:
                        student_name, student_branch, student_cgpa, student_skills, status, app_id = app
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"👤 {student_name} ({student_branch}, CGPA: {student_cgpa})")
                            if student_skills:
                                st.write(f"Skills: {student_skills}")
                        
                        with col2:
                            new_status = st.selectbox(
                                "Status", 
                                ['Applied', 'Shortlisted', 'Rejected', 'Selected'],
                                index=['Applied', 'Shortlisted', 'Rejected', 'Selected'].index(status),
                                key=f"status_{app_id}"
                            )
                            
                            if new_status != status:
                                cursor.execute('UPDATE applications SET status = ? WHERE id = ?', 
                                             (new_status, app_id))
                                conn.commit()
                                success_msg = f"Status updated for {student_name}"
                                st.success(success_msg)
                                simple_tts(success_msg)
                                st.rerun()
    else:
        st.info("You haven't posted any jobs yet.")
    
    conn.close()

def show_post_job():
    """Post job page"""
    if not st.session_state.user_id or st.session_state.user_role != 'company':
        st.error("Access denied.")
        return
    
    st.title("➕ Post New Job")
    
    with st.form("post_job_form"):
        title = st.text_input("Job Title*")
        description = st.text_area("Job Description*", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            min_cgpa = st.number_input("Minimum CGPA*", min_value=0.0, max_value=10.0, step=0.1)
            required_branch = st.selectbox("Required Branch*", [
                "", "Computer Science", "Information Technology", "Electronics", 
                "Mechanical", "Civil", "Electrical", "Any"
            ])
        
        with col2:
            salary = st.text_input("Salary (optional)", placeholder="e.g., 5-8 LPA")
            location = st.text_input("Location (optional)")
        
        required_skills = st.text_area("Required Skills* (comma separated)", 
                                     placeholder="e.g., Python, Java, React, Node.js")
        
        submit = st.form_submit_button("Post Job")
        
        if submit:
            if not all([title, description, min_cgpa, required_branch, required_skills]):
                st.warning("Please fill in all required fields marked with *")
            else:
                conn = sqlite3.connect('job_dekho_simple.db')
                cursor = conn.cursor()
                
                cursor.execute('SELECT id FROM companies WHERE user_id = ?', (st.session_state.user_id,))
                company_id = cursor.fetchone()[0]
                
                cursor.execute('''
                    INSERT INTO jobs (company_id, title, description, min_cgpa, required_branch, 
                                    required_skills, salary, location)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (company_id, title, description, min_cgpa, required_branch, 
                     required_skills, salary, location))
                
                conn.commit()
                conn.close()
                
                success_msg = f"Job '{title}' posted successfully!"
                st.success(success_msg)
                simple_tts(success_msg)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'company_dashboard'
        st.rerun()

def main():
    """Main application"""
    show_sidebar()
    
    # Route to appropriate page
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'login':
        show_login()
    elif st.session_state.page == 'register':
        show_register()
    elif st.session_state.page == 'student_dashboard':
        show_student_dashboard()
    elif st.session_state.page == 'company_dashboard':
        show_company_dashboard()
    elif st.session_state.page == 'post_job':
        show_post_job()
    else:
        show_home()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>🏢 Job Dekho - Smart Job Portal with Voice Assistance | Built with Streamlit & TTS</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()