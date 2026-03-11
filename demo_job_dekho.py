"""
Job Dekho - Standalone Demo
Demonstrates the core functionality without Streamlit
"""

import sqlite3
import hashlib
from datetime import datetime
import os

# Simple TTS function
def simple_tts(text):
    """Simple TTS using Windows SAPI"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        print(f"🔊 TTS: '{text}'")
        return True
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        return False

# Database functions
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('job_dekho_demo.db')
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
    print("✅ Database initialized successfully!")

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_sample_data():
    """Create sample data for demonstration"""
    conn = sqlite3.connect('job_dekho_demo.db')
    cursor = conn.cursor()
    
    try:
        # Create sample users
        password_hash = hash_password("demo123")
        
        # Student user
        cursor.execute('''
            INSERT OR IGNORE INTO users (email, password_hash, role) 
            VALUES (?, ?, ?)
        ''', ("john.doe@student.com", password_hash, "student"))
        student_user_id = cursor.lastrowid or 1
        
        # Company user  
        cursor.execute('''
            INSERT OR IGNORE INTO users (email, password_hash, role) 
            VALUES (?, ?, ?)
        ''', ("hr@techcorp.com", password_hash, "company"))
        company_user_id = cursor.lastrowid or 2
        
        # Create sample student profile
        cursor.execute('''
            INSERT OR IGNORE INTO students (user_id, name, roll_number, cgpa, branch, skills, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_user_id, "Jatin Bulla", "CS2021001", 8.5, "Computer Science", "Python, Java, React, SQL", "9876543210"))
        
        # Create sample company profile
        cursor.execute('''
            INSERT OR IGNORE INTO companies (user_id, name, industry, description, website, contact_person)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (company_user_id, "TechCorp Solutions", "Software Development", 
              "Leading software company specializing in AI and machine learning solutions",
              "https://techcorp.com", "Jane Smith"))
        
        # Create sample jobs
        company_id = cursor.execute('SELECT id FROM companies WHERE user_id = ?', (company_user_id,)).fetchone()[0]
        
        jobs = [
            ("Software Developer", "Develop and maintain web applications using Python and React", 
             7.0, "Computer Science", "Python, React, JavaScript", "6-8 LPA", "Bangalore"),
            ("Data Scientist", "Work with machine learning models and big data analytics", 
             8.0, "Computer Science", "Python, Machine Learning, SQL", "8-12 LPA", "Hyderabad"),
            ("Frontend Developer", "Create responsive user interfaces using modern JavaScript frameworks", 
             6.5, "Any", "JavaScript, React, HTML, CSS", "5-7 LPA", "Mumbai")
        ]
        
        for job in jobs:
            cursor.execute('''
                INSERT OR IGNORE INTO jobs (company_id, title, description, min_cgpa, required_branch, 
                                          required_skills, salary, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company_id,) + job)
        
        conn.commit()
        print("✅ Sample data created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        conn.rollback()
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

def demonstrate_job_matching():
    """Demonstrate the job matching functionality"""
    print("\n🎯 JOB DEKHO - SMART JOB MATCHING DEMO")
    print("=" * 50)
    
    simple_tts("Welcome to Job Dekho, the smart job matching platform!")
    
    conn = sqlite3.connect('job_dekho_demo.db')
    cursor = conn.cursor()
    
    # Get student data
    cursor.execute('''
        SELECT name, roll_number, cgpa, branch, skills, phone 
        FROM students WHERE roll_number = 'CS2021001'
    ''')
    student = cursor.fetchone()
    
    if not student:
        print("❌ No student data found!")
        return
    
    name, roll_number, cgpa, branch, skills, phone = student
    
    print(f"\n👤 STUDENT PROFILE:")
    print(f"   Name: {name}")
    print(f"   Roll Number: {roll_number}")
    print(f"   CGPA: {cgpa}")
    print(f"   Branch: {branch}")
    print(f"   Skills: {skills}")
    
    simple_tts(f"Student profile loaded for {name}")
    
    # Get all jobs
    cursor.execute('''
        SELECT j.id, j.title, j.description, j.min_cgpa, j.required_branch, 
               j.required_skills, j.salary, j.location, c.name as company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        WHERE j.is_active = 1
        ORDER BY j.created_at DESC
    ''')
    jobs = cursor.fetchall()
    
    print(f"\n💼 AVAILABLE JOBS ({len(jobs)} found):")
    print("-" * 50)
    
    job_matches = []
    
    for job in jobs:
        job_id, title, description, min_cgpa, req_branch, req_skills, salary, location, company_name = job
        
        # Calculate match score
        score = calculate_match_score(cgpa, branch, skills, min_cgpa, req_branch, req_skills)
        job_matches.append((score, job))
        
        # Determine match quality
        if score >= 80:
            match_quality = "🎯 EXCELLENT MATCH"
            color = "🟢"
        elif score >= 60:
            match_quality = "⚠️  GOOD MATCH"
            color = "🟡"
        elif score >= 40:
            match_quality = "ℹ️  PARTIAL MATCH"
            color = "🔵"
        else:
            match_quality = "❌ POOR MATCH"
            color = "🔴"
        
        print(f"\n{color} JOB #{job_id}: {title} at {company_name}")
        print(f"   📊 Match Score: {score}% - {match_quality}")
        print(f"   📄 Description: {description}")
        print(f"   📈 Required CGPA: {min_cgpa}+ (You have: {cgpa})")
        print(f"   🎓 Required Branch: {req_branch}")
        print(f"   🔧 Required Skills: {req_skills}")
        if salary:
            print(f"   💰 Salary: {salary}")
        if location:
            print(f"   📍 Location: {location}")
    
    # Sort by score and announce best matches
    job_matches.sort(reverse=True)
    
    print(f"\n🏆 TOP RECOMMENDATIONS:")
    print("-" * 30)
    
    for i, (score, job) in enumerate(job_matches[:3]):
        job_id, title, description, min_cgpa, req_branch, req_skills, salary, location, company_name = job
        print(f"{i+1}. {title} at {company_name} ({score}% match)")
        
        if i == 0:  # Announce the best match
            announcement = f"Your best job match is {title} at {company_name} with {score} percent compatibility"
            simple_tts(announcement)
    
    # Simulate application
    if job_matches and job_matches[0][0] >= 80:
        best_job = job_matches[0][1]
        job_id = best_job[0]
        title = best_job[1]
        
        print(f"\n🚀 AUTO-APPLYING to best match: {title}")
        
        # Get student ID
        cursor.execute('SELECT id FROM students WHERE roll_number = ?', (roll_number,))
        student_id = cursor.fetchone()[0]
        
        # Apply for job (simulate)
        status = "Shortlisted" if job_matches[0][0] >= 90 else "Applied"
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO applications (student_id, job_id, status)
                VALUES (?, ?, ?)
            ''', (student_id, job_id, status))
            conn.commit()
            
            if status == 'Shortlisted':
                success_msg = f"🎉 Congratulations! You've been automatically shortlisted for {title}!"
                print(success_msg)
                simple_tts("Congratulations! You have been automatically shortlisted!")
            else:
                success_msg = f"✅ Application submitted successfully for {title}!"
                print(success_msg)
                simple_tts("Application submitted successfully!")
                
        except Exception as e:
            print(f"❌ Error applying for job: {e}")
    
    conn.close()

def show_application_status():
    """Show application status"""
    print(f"\n📋 APPLICATION STATUS:")
    print("-" * 30)
    
    conn = sqlite3.connect('job_dekho_demo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT j.title, c.name, a.status, a.applied_at
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN jobs j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        WHERE s.roll_number = 'CS2021001'
        ORDER BY a.applied_at DESC
    ''')
    
    applications = cursor.fetchall()
    
    if applications:
        for i, (title, company, status, applied_at) in enumerate(applications, 1):
            status_icon = "🎉" if status == "Shortlisted" else "✅" if status == "Applied" else "❌"
            print(f"{i}. {status_icon} {title} at {company}")
            print(f"   Status: {status}")
            print(f"   Applied: {applied_at}")
            
        simple_tts(f"You have {len(applications)} job applications")
    else:
        print("No applications found.")
    
    conn.close()

def test_tts_functionality():
    """Test TTS functionality"""
    print(f"\n🔊 TESTING TTS FUNCTIONALITY:")
    print("-" * 35)
    
    test_messages = [
        "Welcome to Job Dekho!",
        "Your profile has been created successfully!",
        "New job match found with 95 percent compatibility!",
        "You have been shortlisted for Software Developer position!",
        "Thank you for using Job Dekho!"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"{i}. Testing: '{message}'")
        if simple_tts(message):
            print("   ✅ TTS working")
        else:
            print("   ❌ TTS failed")
        print()

def main():
    """Main demo function"""
    print("🏢 JOB DEKHO - SMART JOB PORTAL WITH TTS")
    print("=" * 60)
    print("Setting up demo environment...")
    
    # Initialize database and create sample data
    init_database()
    create_sample_data()
    
    # Test TTS functionality
    test_tts_functionality()
    
    # Demonstrate job matching
    demonstrate_job_matching()
    
    # Show application status
    show_application_status()
    
    print(f"\n🎯 DEMO COMPLETED!")
    print("=" * 30)
    print("Key features demonstrated:")
    print("✅ Database setup and management")
    print("✅ User profiles (Students & Companies)")
    print("✅ Job posting and management")
    print("✅ Smart matching algorithm")
    print("✅ Automatic shortlisting")
    print("✅ Text-to-Speech announcements")
    print("✅ Application tracking")
    
    simple_tts("Demo completed! Thank you for using Job Dekho!")
    
    # Show database file location
    db_path = os.path.abspath('job_dekho_demo.db')
    print(f"\n💾 Database created at: {db_path}")

if __name__ == "__main__":
    main()