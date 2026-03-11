"""
Database Initialization Script for JOB DEKHO
Creates all tables and populates with sample data for testing
"""

from app import app
from database import db
from models import User, Student, Company, Job, Application, Admin
from datetime import datetime, timedelta
import os

def init_database():
    """Initialize database and create all tables"""
    with app.app_context():
        # Drop all tables (for fresh start)
        print("🗑️  Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("📦 Creating database tables...")
        db.create_all()
        print("✅ Tables created successfully!\n")
        
        # Create Admin User
        print("👤 Creating admin user...")
        admin_user = User(
            email='admin@jobdekho.com',
            role='admin',
            is_active=True
        )
        admin_user.set_password('admin123')
        admin_user.last_login = datetime.utcnow()
        db.session.add(admin_user)
        db.session.flush()
        
        admin = Admin(
            user_id=admin_user.id,
            name='System Administrator',
            phone='9876543210'
        )
        db.session.add(admin)
        print(f"  ✓ Admin: {admin_user.email} / admin123")
        
        # Create Sample Students
        print("\n👨‍🎓 Creating sample students...")
        students_data = [
            {
                'email': 'rahul.sharma@student.com',
                'password': 'student123',
                'name': 'Rahul Sharma',
                'roll_number': 'CS2021001',
                'cgpa': 8.5,
                'branch': 'Computer Science',
                'skills': 'Python, Java, Machine Learning, Data Structures',
                'phone': '9876501234'
            },
            {
                'email': 'priya.patel@student.com',
                'password': 'student123',
                'name': 'Priya Patel',
                'roll_number': 'CS2021002',
                'cgpa': 9.2,
                'branch': 'Computer Science',
                'skills': 'JavaScript, React, Node.js, MongoDB, AWS',
                'phone': '9876501235'
            },
            {
                'email': 'amit.kumar@student.com',
                'password': 'student123',
                'name': 'Amit Kumar',
                'roll_number': 'EC2021001',
                'cgpa': 7.8,
                'branch': 'Electronics',
                'skills': 'C++, Embedded Systems, IoT, Arduino',
                'phone': '9876501236'
            },
            {
                'email': 'sneha.reddy@student.com',
                'password': 'student123',
                'name': 'Sneha Reddy',
                'roll_number': 'CS2021003',
                'cgpa': 8.9,
                'branch': 'Computer Science',
                'skills': 'Python, Django, PostgreSQL, Docker, Kubernetes',
                'phone': '9876501237'
            },
            {
                'email': 'vikram.singh@student.com',
                'password': 'student123',
                'name': 'Vikram Singh',
                'roll_number': 'ME2021001',
                'cgpa': 7.5,
                'branch': 'Mechanical',
                'skills': 'CAD, AutoCAD, SolidWorks, Manufacturing',
                'phone': '9876501238'
            }
        ]
        
        for s_data in students_data:
            user = User(
                email=s_data['email'],
                role='student',
                is_active=True
            )
            user.set_password(s_data['password'])
            user.last_login = datetime.utcnow() - timedelta(days=2)
            db.session.add(user)
            db.session.flush()
            
            student = Student(
                user_id=user.id,
                name=s_data['name'],
                roll_number=s_data['roll_number'],
                cgpa=s_data['cgpa'],
                branch=s_data['branch'],
                skills=s_data['skills'],
                phone=s_data['phone']
            )
            db.session.add(student)
            print(f"  ✓ {s_data['name']} ({s_data['email']})")
        
        # Create Sample Companies
        print("\n🏢 Creating sample companies...")
        companies_data = [
            {
                'email': 'hr@techcorp.com',
                'password': 'company123',
                'name': 'TechCorp Solutions',
                'industry': 'Information Technology',
                'description': 'Leading IT solutions provider specializing in web and mobile applications',
                'website': 'https://techcorp.com',
                'contact_person': 'Rajesh Kumar'
            },
            {
                'email': 'careers@innovate.com',
                'password': 'company123',
                'name': 'Innovate Systems',
                'industry': 'Software Development',
                'description': 'Innovative software company focused on AI and Machine Learning solutions',
                'website': 'https://innovatesys.com',
                'contact_person': 'Anita Desai'
            },
            {
                'email': 'jobs@datatech.com',
                'password': 'company123',
                'name': 'DataTech Analytics',
                'industry': 'Data Analytics',
                'description': 'Data-driven solutions for business intelligence and analytics',
                'website': 'https://datatech.com',
                'contact_person': 'Suresh Menon'
            },
            {
                'email': 'recruit@cloudnine.com',
                'password': 'company123',
                'name': 'CloudNine Technologies',
                'industry': 'Cloud Computing',
                'description': 'Cloud infrastructure and DevOps solutions provider',
                'website': 'https://cloudnine.com',
                'contact_person': 'Meera Shah'
            }
        ]
        
        company_objects = []
        for c_data in companies_data:
            user = User(
                email=c_data['email'],
                role='company',
                is_active=True
            )
            user.set_password(c_data['password'])
            user.last_login = datetime.utcnow() - timedelta(days=1)
            db.session.add(user)
            db.session.flush()
            
            company = Company(
                user_id=user.id,
                name=c_data['name'],
                industry=c_data['industry'],
                description=c_data['description'],
                website=c_data['website'],
                contact_person=c_data['contact_person']
            )
            db.session.add(company)
            company_objects.append(company)
            print(f"  ✓ {c_data['name']} ({c_data['email']})")
        
        db.session.flush()
        
        # Create Sample Jobs
        print("\n💼 Creating sample job postings...")
        jobs_data = [
            {
                'company': 0,  # TechCorp
                'title': 'Full Stack Developer',
                'description': 'Looking for a talented full stack developer with experience in React and Node.js. You will work on exciting projects building scalable web applications.',
                'min_cgpa': 7.5,
                'required_branch': 'Computer Science',
                'required_skills': 'JavaScript, React, Node.js, MongoDB',
                'salary': '₹6-8 LPA',
                'location': 'Bangalore',
                'job_type': 'Full-time'
            },
            {
                'company': 0,  # TechCorp
                'title': 'Backend Developer',
                'description': 'We need a backend developer proficient in Python and Django to build robust APIs and server-side applications.',
                'min_cgpa': 7.0,
                'required_branch': 'Computer Science',
                'required_skills': 'Python, Django, PostgreSQL, Docker',
                'salary': '₹5-7 LPA',
                'location': 'Pune',
                'job_type': 'Full-time'
            },
            {
                'company': 1,  # Innovate Systems
                'title': 'Machine Learning Engineer',
                'description': 'Join our AI team to develop cutting-edge machine learning models. Experience with Python and ML frameworks required.',
                'min_cgpa': 8.0,
                'required_branch': 'Computer Science',
                'required_skills': 'Python, Machine Learning, TensorFlow, Data Structures',
                'salary': '₹8-12 LPA',
                'location': 'Hyderabad',
                'job_type': 'Full-time'
            },
            {
                'company': 1,  # Innovate Systems
                'title': 'Data Science Intern',
                'description': 'Internship opportunity for students interested in data science and analytics. Hands-on experience with real-world projects.',
                'min_cgpa': 7.5,
                'required_branch': 'Computer Science',
                'required_skills': 'Python, Machine Learning, Data Analysis',
                'salary': '₹25,000/month',
                'location': 'Remote',
                'job_type': 'Internship'
            },
            {
                'company': 2,  # DataTech
                'title': 'Data Analyst',
                'description': 'Seeking a data analyst to help clients make data-driven decisions. Experience with SQL and visualization tools required.',
                'min_cgpa': 7.0,
                'required_branch': 'Computer Science',
                'required_skills': 'Python, SQL, Data Analysis, Excel',
                'salary': '₹4-6 LPA',
                'location': 'Mumbai',
                'job_type': 'Full-time'
            },
            {
                'company': 3,  # CloudNine
                'title': 'DevOps Engineer',
                'description': 'Looking for a DevOps engineer to manage our cloud infrastructure. Experience with AWS, Docker, and Kubernetes preferred.',
                'min_cgpa': 7.5,
                'required_branch': 'Computer Science',
                'required_skills': 'AWS, Docker, Kubernetes, Linux',
                'salary': '₹7-10 LPA',
                'location': 'Bangalore',
                'job_type': 'Full-time'
            },
            {
                'company': 3,  # CloudNine
                'title': 'Cloud Infrastructure Intern',
                'description': 'Internship for students interested in cloud computing and infrastructure management.',
                'min_cgpa': 7.0,
                'required_branch': 'Computer Science',
                'required_skills': 'AWS, Docker, Linux',
                'salary': '₹20,000/month',
                'location': 'Bangalore',
                'job_type': 'Internship'
            }
        ]
        
        job_objects = []
        for j_data in jobs_data:
            job = Job(
                company_id=company_objects[j_data['company']].id,
                title=j_data['title'],
                description=j_data['description'],
                min_cgpa=j_data['min_cgpa'],
                required_branch=j_data['required_branch'],
                required_skills=j_data['required_skills'],
                salary=j_data['salary'],
                location=j_data['location'],
                job_type=j_data['job_type'],
                is_active=True
            )
            db.session.add(job)
            job_objects.append(job)
            print(f"  ✓ {j_data['title']} at {company_objects[j_data['company']].name}")
        
        db.session.flush()
        
        # Create Sample Applications
        print("\n📝 Creating sample applications...")
        students = Student.query.all()
        
        # Rahul applies to Full Stack Developer
        app1 = Application(
            student_id=students[0].id,
            job_id=job_objects[0].id,
            status='Shortlisted',
            applied_at=datetime.utcnow() - timedelta(days=5),
            match_score=85.0
        )
        db.session.add(app1)
        
        # Priya applies to Machine Learning Engineer
        app2 = Application(
            student_id=students[1].id,
            job_id=job_objects[2].id,
            status='Selected',
            applied_at=datetime.utcnow() - timedelta(days=10),
            match_score=95.0
        )
        db.session.add(app2)
        
        # Sneha applies to DevOps Engineer
        app3 = Application(
            student_id=students[3].id,
            job_id=job_objects[5].id,
            status='Applied',
            applied_at=datetime.utcnow() - timedelta(days=2),
            match_score=88.0
        )
        db.session.add(app3)
        
        # Rahul applies to Backend Developer
        app4 = Application(
            student_id=students[0].id,
            job_id=job_objects[1].id,
            status='Applied',
            applied_at=datetime.utcnow() - timedelta(days=3),
            match_score=75.0
        )
        db.session.add(app4)
        
        print("  ✓ Sample applications created")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*60)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("="*60)
        print("\n📋 TEST ACCOUNTS:")
        print("\n  👤 ADMIN:")
        print("     Email: admin@jobdekho.com")
        print("     Password: admin123")
        print("\n  👨‍🎓 STUDENTS (all have password: student123):")
        for s_data in students_data:
            print(f"     {s_data['email']} - {s_data['name']} (CGPA: {s_data['cgpa']})")
        print("\n  🏢 COMPANIES (all have password: company123):")
        for c_data in companies_data:
            print(f"     {c_data['email']} - {c_data['name']}")
        print("\n" + "="*60)
        print("🚀 You can now run: python app.py")
        print("="*60 + "\n")

if __name__ == '__main__':
    init_database()
