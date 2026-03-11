from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'company', or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    student = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    company = db.relationship('Company', backref='user', uselist=False, cascade='all, delete-orphan')
    admin = db.relationship('Admin', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.Text)  # Comma-separated skills
    phone = db.Column(db.String(15))
    resume_path = db.Column(db.String(255))  # Path to uploaded resume
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.name}>'


class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    contact_person = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    jobs = db.relationship('Job', backref='company', lazy=True)
    
    def __repr__(self):
        return f'<Company {self.name}>'


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    required_branch = db.Column(db.String(100), nullable=False)
    required_skills = db.Column(db.Text)  # Comma-separated skills
    salary = db.Column(db.String(50))
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(20), default='Full-time')  # Full-time, Part-time, Internship
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True)
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company.name}>'


class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    status = db.Column(db.String(20), default='Applied')  # Applied, Shortlisted, Interview, Rejected, Selected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    match_score = db.Column(db.Float, default=0.0)  # Matching score from algorithm
    
    # Composite unique constraint to prevent duplicate applications
    __table_args__ = (db.UniqueConstraint('student_id', 'job_id', name='unique_student_job_application'),)
    
    def __repr__(self):
        return f'<Application {self.student.name} -> {self.job.title}>'


class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Admin {self.name}>'
