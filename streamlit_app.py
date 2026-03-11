"""
Job Dekho - Streamlit Application with TTS
An intelligent job matching platform with text-to-speech functionality
"""

import streamlit as st
import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

# Import our modules
from streamlit_models import (
    User, Student, Company, Job, Application,
    SessionLocal, create_tables
)
from tts_utils import (
    add_tts_controls, announce_page_title, announce_notification,
    speak_text, create_tts_button, create_job_card_with_tts, test_tts
)
from matching_algorithm import auto_shortlist, get_matching_score

# Page configuration
st.set_page_config(
    page_title="Job Dekho - Smart Job Portal with TTS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
create_tables()


def get_db_session():
    """Get database session"""
    return SessionLocal()


def init_session_state():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'


def logout():
    """Logout user"""
    st.session_state.user_id = None
    st.session_state.user_role = None
    st.session_state.user_email = None
    st.session_state.page = 'home'
    announce_notification("You have been logged out", "info")


def authenticate_user(email, password):
    """Authenticate user"""
    db = get_db_session()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return None
    finally:
        db.close()


def register_user(user_data):
    """Register new user"""
    db = get_db_session()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data['email']).first()
        if existing_user:
            return False, "Email already registered!"
        
        # Create new user
        new_user = User(
            email=user_data['email'],
            role=user_data['role']
        )
        new_user.set_password(user_data['password'])
        db.add(new_user)
        db.flush()  # Get user ID
        
        # Create profile based on role
        if user_data['role'] == 'student':
            student = Student(
                user_id=new_user.id,
                name=user_data['name'],
                roll_number=user_data['roll_number'],
                cgpa=user_data['cgpa'],
                branch=user_data['branch'],
                skills=user_data['skills'],
                phone=user_data.get('phone', '')
            )
            db.add(student)
        
        elif user_data['role'] == 'company':
            company = Company(
                user_id=new_user.id,
                name=user_data['name'],
                industry=user_data.get('industry', ''),
                description=user_data.get('description', ''),
                website=user_data.get('website', ''),
                contact_person=user_data.get('contact_person', '')
            )
            db.add(company)
        
        db.commit()
        return True, "Registration successful!"
        
    except Exception as e:
        db.rollback()
        return False, f"Registration failed: {str(e)}"
    finally:
        db.close()


def show_home_page():
    """Show home page"""
    announce_page_title("Home")
    
    st.title("🏢 Job Dekho - Smart Job Portal")
    st.markdown("### Your intelligent job matching platform with voice assistance")
    
    # Add TTS button for page description
    page_description = """
    Welcome to Job Dekho, an intelligent job matching platform that connects students with companies. 
    Our smart algorithm automatically matches candidates based on their skills, CGPA, and branch preferences.
    This platform includes text-to-speech functionality to make it accessible for everyone.
    """
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(page_description)
    with col2:
        create_tts_button(page_description, key="home_desc", help_text="Listen to page description")
    
    if not st.session_state.user_id:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎓 For Students")
            st.markdown("""
            - Find jobs that match your skills and qualifications
            - Upload your resume and get automatically shortlisted
            - Track your applications with real-time status updates
            - Listen to job descriptions with text-to-speech
            """)
            if st.button("Register as Student", key="reg_student"):
                st.session_state.page = 'register'
                st.rerun()
        
        with col2:
            st.subheader("🏢 For Companies")
            st.markdown("""
            - Post job openings with detailed requirements
            - Get automatically matched candidates
            - Manage applications and update status
            - Access voice-guided interface
            """)
            if st.button("Register as Company", key="reg_company"):
                st.session_state.page = 'register'
                st.rerun()
        
        st.markdown("---")
        st.markdown("**Already have an account?**")
        if st.button("Login Here", key="goto_login"):
            st.session_state.page = 'login'
            st.rerun()
    
    else:
        st.success(f"Welcome back, {st.session_state.user_email}!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.user_role == 'student':
                if st.button("Go to Student Dashboard", key="goto_student_dash"):
                    st.session_state.page = 'student_dashboard'
                    st.rerun()
            elif st.session_state.user_role == 'company':
                if st.button("Go to Company Dashboard", key="goto_company_dash"):
                    st.session_state.page = 'company_dashboard'
                    st.rerun()
        
        with col2:
            if st.button("Logout", key="logout_home"):
                logout()
                st.rerun()


def show_login_page():
    """Show login page"""
    announce_page_title("Login")
    
    st.title("🔐 Login to Job Dekho")
    
    with st.form("login_form"):
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if email and password:
                user = authenticate_user(email, password)
                if user:
                    st.session_state.user_id = user.id
                    st.session_state.user_role = user.role
                    st.session_state.user_email = user.email
                    
                    success_msg = f"Welcome back! Logged in as {user.role}"
                    st.success(success_msg)
                    announce_notification(success_msg, "success")
                    
                    # Redirect based on role
                    if user.role == 'student':
                        st.session_state.page = 'student_dashboard'
                    else:
                        st.session_state.page = 'company_dashboard'
                    st.rerun()
                else:
                    error_msg = "Invalid email or password!"
                    st.error(error_msg)
                    announce_notification(error_msg, "error")
            else:
                warning_msg = "Please enter both email and password"
                st.warning(warning_msg)
                announce_notification(warning_msg, "warning")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Home", key="login_back"):
            st.session_state.page = 'home'
            st.rerun()
    with col2:
        if st.button("Register New Account", key="login_to_register"):
            st.session_state.page = 'register'
            st.rerun()


def show_register_page():
    """Show registration page"""
    announce_page_title("Registration")
    
    st.title("📝 Register for Job Dekho")
    
    with st.form("register_form"):
        # Basic information
        st.subheader("Basic Information")
        email = st.text_input("Email Address*", key="reg_email")
        password = st.text_input("Password*", type="password", key="reg_password")
        role = st.selectbox("I am a:", ["", "student", "company"], key="reg_role")
        
        # Role-specific fields
        if role == "student":
            st.subheader("Student Information")
            name = st.text_input("Full Name*", key="reg_student_name")
            roll_number = st.text_input("Roll Number*", key="reg_roll_number")
            cgpa = st.number_input("CGPA*", min_value=0.0, max_value=10.0, step=0.01, key="reg_cgpa")
            branch = st.selectbox("Branch*", [
                "", "Computer Science", "Information Technology", "Electronics", 
                "Mechanical", "Civil", "Electrical", "Other"
            ], key="reg_branch")
            skills = st.text_area("Skills (comma separated)*", 
                                placeholder="e.g., Python, Java, React, Node.js", key="reg_skills")
            phone = st.text_input("Phone Number", key="reg_phone")
            
        elif role == "company":
            st.subheader("Company Information")
            name = st.text_input("Company Name*", key="reg_company_name")
            industry = st.text_input("Industry", key="reg_industry")
            description = st.text_area("Company Description", key="reg_description")
            website = st.text_input("Website", key="reg_website")
            contact_person = st.text_input("Contact Person", key="reg_contact")
        
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            # Validation
            if not email or not password or not role:
                warning_msg = "Please fill in all required fields marked with *"
                st.warning(warning_msg)
                announce_notification(warning_msg, "warning")
                return
            
            if role == "student" and not all([name, roll_number, cgpa, branch, skills]):
                warning_msg = "Please fill in all required student information"
                st.warning(warning_msg)
                announce_notification(warning_msg, "warning")
                return
            
            if role == "company" and not name:
                warning_msg = "Please enter company name"
                st.warning(warning_msg)
                announce_notification(warning_msg, "warning")
                return
            
            # Prepare user data
            user_data = {
                'email': email,
                'password': password,
                'role': role,
                'name': name
            }
            
            if role == "student":
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
            
            # Register user
            success, message = register_user(user_data)
            if success:
                st.success(message)
                announce_notification(message, "success")
                st.info("Please login with your new account.")
                if st.button("Go to Login"):
                    st.session_state.page = 'login'
                    st.rerun()
            else:
                st.error(message)
                announce_notification(message, "error")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Home", key="register_back"):
            st.session_state.page = 'home'
            st.rerun()
    with col2:
        if st.button("Already have an account? Login", key="register_to_login"):
            st.session_state.page = 'login'
            st.rerun()


def show_student_dashboard():
    """Show student dashboard"""
    if not st.session_state.user_id or st.session_state.user_role != 'student':
        st.error("Access denied. Please login as a student.")
        return
    
    announce_page_title("Student Dashboard")
    
    st.title("🎓 Student Dashboard")
    
    db = get_db_session()
    try:
        # Get student data
        student = db.query(Student).filter(Student.user_id == st.session_state.user_id).first()
        if not student:
            st.error("Student profile not found.")
            return
        
        # Welcome message with TTS
        welcome_msg = f"Welcome back, {student.name}!"
        st.subheader(welcome_msg)
        create_tts_button(welcome_msg, key="welcome_msg", help_text="Listen to welcome message")
        
        # Profile summary
        with st.expander("📋 Your Profile", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("CGPA", student.cgpa)
            with col2:
                st.metric("Branch", student.branch)
            with col3:
                st.metric("Roll Number", student.roll_number)
            
            if student.skills:
                st.write(f"**Skills:** {student.skills}")
            if student.phone:
                st.write(f"**Phone:** {student.phone}")
        
        # Get applications and jobs
        applications = db.query(Application).filter(Application.student_id == student.id).all()
        jobs = db.query(Job).filter(Job.is_active == True).all()
        
        # Statistics
        st.subheader("📊 Your Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Applications", len(applications))
        with col2:
            shortlisted = len([app for app in applications if app.status == 'Shortlisted'])
            st.metric("Shortlisted", shortlisted)
        with col3:
            st.metric("Available Jobs", len(jobs))
        
        # Available Jobs
        st.subheader("💼 Available Jobs")
        if jobs:
            for job in jobs:
                # Check if already applied
                already_applied = any(app.job_id == job.id for app in applications)
                
                with st.expander(f"🏢 {job.title} at {job.company.name if job.company else 'Unknown'}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Description:** {job.description}")
                        st.write(f"**Required CGPA:** {job.min_cgpa}+")
                        st.write(f"**Branch:** {job.required_branch}")
                        st.write(f"**Skills:** {job.required_skills}")
                        if job.salary:
                            st.write(f"**Salary:** {job.salary}")
                        if job.location:
                            st.write(f"**Location:** {job.location}")
                        
                        # Show matching score
                        score = get_matching_score(student, job)
                        if score >= 70:
                            st.success(f"🎯 Excellent Match: {score}% compatibility")
                        elif score >= 50:
                            st.warning(f"⚠️ Good Match: {score}% compatibility")
                        else:
                            st.info(f"ℹ️ Partial Match: {score}% compatibility")
                    
                    with col2:
                        # TTS for job details
                        job_text = f"""
                        Job: {job.title} at {job.company.name if job.company else 'Unknown Company'}
                        Description: {job.description}
                        Required CGPA: {job.min_cgpa} or above
                        Branch: {job.required_branch}
                        Skills: {job.required_skills}
                        Compatibility: {score} percent
                        """
                        if job.salary:
                            job_text += f"Salary: {job.salary}"
                        if job.location:
                            job_text += f"Location: {job.location}"
                        
                        create_tts_button(job_text.strip(), 
                                        key=f"job_tts_{job.id}", 
                                        help_text="Listen to job details")
                        
                        if already_applied:
                            app = next(app for app in applications if app.job_id == job.id)
                            st.success(f"Applied ✓\\n({app.status})")
                        else:
                            if st.button(f"Apply Now", key=f"apply_{job.id}"):
                                # Apply for job
                                status = auto_shortlist(student, job)
                                new_application = Application(
                                    student_id=student.id,
                                    job_id=job.id,
                                    status=status
                                )
                                db.add(new_application)
                                db.commit()
                                
                                if status == 'Shortlisted':
                                    success_msg = f"Congratulations! You've been automatically shortlisted for {job.title}!"
                                    st.success(success_msg)
                                    announce_notification(success_msg, "success")
                                else:
                                    success_msg = f"Application submitted for {job.title}!"
                                    st.success(success_msg)
                                    announce_notification(success_msg, "success")
                                
                                st.rerun()
        else:
            st.info("No jobs available at the moment.")
        
        # Your Applications
        if applications:
            st.subheader("📋 Your Applications")
            for app in applications:
                with st.expander(f"Application: {app.job.title} - Status: {app.status}"):
                    st.write(f"**Company:** {app.job.company.name}")
                    st.write(f"**Applied on:** {app.applied_at.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Status:** {app.status}")
                    
                    # Status color coding
                    if app.status == 'Shortlisted':
                        st.success("🎉 You've been shortlisted!")
                    elif app.status == 'Selected':
                        st.success("🎊 Congratulations! You've been selected!")
                    elif app.status == 'Rejected':
                        st.error("❌ Application rejected")
                    else:
                        st.info("⏳ Application under review")
        
        # Profile update section
        if st.button("Update Profile", key="update_profile"):
            st.session_state.page = 'update_profile'
            st.rerun()
    
    finally:
        db.close()


def show_company_dashboard():
    """Show company dashboard"""
    if not st.session_state.user_id or st.session_state.user_role != 'company':
        st.error("Access denied. Please login as a company.")
        return
    
    announce_page_title("Company Dashboard")
    
    st.title("🏢 Company Dashboard")
    
    db = get_db_session()
    try:
        # Get company data
        company = db.query(Company).filter(Company.user_id == st.session_state.user_id).first()
        if not company:
            st.error("Company profile not found.")
            return
        
        # Welcome message with TTS
        welcome_msg = f"Welcome, {company.name}!"
        st.subheader(welcome_msg)
        create_tts_button(welcome_msg, key="company_welcome", help_text="Listen to welcome message")
        
        # Company info
        with st.expander("🏢 Company Information", expanded=True):
            st.write(f"**Industry:** {company.industry or 'Not specified'}")
            if company.description:
                st.write(f"**Description:** {company.description}")
            if company.website:
                st.write(f"**Website:** {company.website}")
            if company.contact_person:
                st.write(f"**Contact Person:** {company.contact_person}")
        
        # Get jobs and applications
        jobs = db.query(Job).filter(Job.company_id == company.id).all()
        job_ids = [job.id for job in jobs]
        applications = db.query(Application).filter(Application.job_id.in_(job_ids)).all() if job_ids else []
        
        # Statistics
        st.subheader("📊 Your Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Jobs Posted", len(jobs))
        with col2:
            st.metric("Total Applications", len(applications))
        with col3:
            shortlisted = len([app for app in applications if app.status == 'Shortlisted'])
            st.metric("Shortlisted Candidates", shortlisted)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Post New Job", key="post_job"):
                st.session_state.page = 'post_job'
                st.rerun()
        with col2:
            if st.button("✏️ Update Profile", key="company_update_profile"):
                st.session_state.page = 'company_update_profile'
                st.rerun()
        
        # Posted Jobs
        if jobs:
            st.subheader("📝 Your Posted Jobs")
            for job in jobs:
                job_applications = [app for app in applications if app.job_id == job.id]
                
                with st.expander(f"📋 {job.title} ({len(job_applications)} applications)"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Description:** {job.description}")
                        st.write(f"**Required CGPA:** {job.min_cgpa}+")
                        st.write(f"**Branch:** {job.required_branch}")
                        st.write(f"**Skills:** {job.required_skills}")
                        if job.salary:
                            st.write(f"**Salary:** {job.salary}")
                        if job.location:
                            st.write(f"**Location:** {job.location}")
                        st.write(f"**Status:** {'Active' if job.is_active else 'Inactive'}")
                        st.write(f"**Posted:** {job.created_at.strftime('%Y-%m-%d')}")
                    
                    with col2:
                        # TTS for job info
                        job_text = f"""
                        Job title: {job.title}
                        Description: {job.description}
                        Applications received: {len(job_applications)}
                        Required CGPA: {job.min_cgpa} or above
                        Required branch: {job.required_branch}
                        Required skills: {job.required_skills}
                        """
                        create_tts_button(job_text.strip(), 
                                        key=f"company_job_tts_{job.id}", 
                                        help_text="Listen to job summary")
                    
                    # Applications for this job
                    if job_applications:
                        st.write("**Applications:**")
                        for app in job_applications:
                            col1, col2, col3 = st.columns([2, 1, 1])
                            with col1:
                                st.write(f"👤 {app.student.name} ({app.student.branch}, CGPA: {app.student.cgpa})")
                            with col2:
                                current_status = app.status
                                new_status = st.selectbox(
                                    "Status", 
                                    ['Applied', 'Shortlisted', 'Rejected', 'Selected'],
                                    index=['Applied', 'Shortlisted', 'Rejected', 'Selected'].index(current_status),
                                    key=f"status_{app.id}"
                                )
                                
                                if new_status != current_status:
                                    app.status = new_status
                                    db.commit()
                                    success_msg = f"Status updated for {app.student.name}"
                                    st.success(success_msg)
                                    announce_notification(success_msg, "success")
                                    st.rerun()
                            
                            with col3:
                                # TTS for candidate info
                                candidate_text = f"""
                                Candidate: {app.student.name}
                                Branch: {app.student.branch}
                                CGPA: {app.student.cgpa}
                                Skills: {app.student.skills or 'Not specified'}
                                Current status: {app.status}
                                """
                                create_tts_button(candidate_text.strip(), 
                                                key=f"candidate_tts_{app.id}", 
                                                help_text="Listen to candidate info")
                    else:
                        st.info("No applications yet for this job.")
        else:
            st.info("You haven't posted any jobs yet.")
    
    finally:
        db.close()


def show_post_job_page():
    """Show post job page"""
    if not st.session_state.user_id or st.session_state.user_role != 'company':
        st.error("Access denied.")
        return
    
    announce_page_title("Post Job")
    
    st.title("➕ Post New Job")
    
    db = get_db_session()
    try:
        company = db.query(Company).filter(Company.user_id == st.session_state.user_id).first()
        
        with st.form("post_job_form"):
            title = st.text_input("Job Title*", key="job_title")
            description = st.text_area("Job Description*", key="job_description", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                min_cgpa = st.number_input("Minimum CGPA*", min_value=0.0, max_value=10.0, step=0.1, key="job_min_cgpa")
                required_branch = st.selectbox("Required Branch*", [
                    "", "Computer Science", "Information Technology", "Electronics", 
                    "Mechanical", "Civil", "Electrical", "Any"
                ], key="job_branch")
            
            with col2:
                salary = st.text_input("Salary (optional)", placeholder="e.g., 5-8 LPA", key="job_salary")
                location = st.text_input("Location (optional)", key="job_location")
                job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Internship"], key="job_type")
            
            required_skills = st.text_area("Required Skills* (comma separated)", 
                                         placeholder="e.g., Python, Java, React, Node.js", key="job_skills")
            
            submit_button = st.form_submit_button("Post Job")
            
            if submit_button:
                if not all([title, description, min_cgpa, required_branch, required_skills]):
                    warning_msg = "Please fill in all required fields marked with *"
                    st.warning(warning_msg)
                    announce_notification(warning_msg, "warning")
                else:
                    # Create job
                    new_job = Job(
                        company_id=company.id,
                        title=title,
                        description=description,
                        min_cgpa=min_cgpa,
                        required_branch=required_branch,
                        required_skills=required_skills,
                        salary=salary,
                        location=location,
                        job_type=job_type
                    )
                    
                    db.add(new_job)
                    db.commit()
                    
                    success_msg = f"Job '{title}' posted successfully!"
                    st.success(success_msg)
                    announce_notification(success_msg, "success")
                    
                    if st.button("Back to Dashboard"):
                        st.session_state.page = 'company_dashboard'
                        st.rerun()
    
    finally:
        db.close()
    
    if st.button("← Back to Dashboard", key="post_job_back"):
        st.session_state.page = 'company_dashboard'
        st.rerun()


def show_sidebar():
    """Show sidebar with navigation and TTS controls"""
    with st.sidebar:
        st.title("🏢 Job Dekho")
        
        # User info
        if st.session_state.user_id:
            st.success(f"✅ Logged in as {st.session_state.user_role}")
            st.caption(f"📧 {st.session_state.user_email}")
            
            # Navigation
            st.markdown("---")
            st.subheader("📱 Navigation")
            
            if st.session_state.user_role == 'student':
                if st.button("🎓 Student Dashboard", key="nav_student_dash"):
                    st.session_state.page = 'student_dashboard'
                    st.rerun()
            elif st.session_state.user_role == 'company':
                if st.button("🏢 Company Dashboard", key="nav_company_dash"):
                    st.session_state.page = 'company_dashboard'
                    st.rerun()
                if st.button("➕ Post Job", key="nav_post_job"):
                    st.session_state.page = 'post_job'
                    st.rerun()
            
            if st.button("🏠 Home", key="nav_home"):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("🚪 Logout", key="nav_logout"):
                logout()
                st.rerun()
        
        else:
            st.info("Not logged in")
            if st.button("🔐 Login", key="nav_login"):
                st.session_state.page = 'login'
                st.rerun()
            if st.button("📝 Register", key="nav_register"):
                st.session_state.page = 'register'
                st.rerun()
        
        # TTS Controls
        st.markdown("---")
        add_tts_controls()
        
        # Quick TTS test
        st.markdown("---")
        st.subheader("🔧 TTS Test")
        test_text = st.text_input("Test TTS:", value="Hello, this is a test!")
        if st.button("🔊 Test Speak", key="test_tts_sidebar"):
            speak_text(test_text)
            st.success("Speaking...")


def main():
    """Main application function"""
    init_session_state()
    
    # Show sidebar
    show_sidebar()
    
    # Show main content based on current page
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'login':
        show_login_page()
    elif st.session_state.page == 'register':
        show_register_page()
    elif st.session_state.page == 'student_dashboard':
        show_student_dashboard()
    elif st.session_state.page == 'company_dashboard':
        show_company_dashboard()
    elif st.session_state.page == 'post_job':
        show_post_job_page()
    else:
        show_home_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🏢 Job Dekho - Smart Job Portal with Voice Assistance | Built with Streamlit & TTS</p>
        </div>
        """, 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()