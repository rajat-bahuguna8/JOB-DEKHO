"""
Database models for Streamlit Job Dekho application
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import bcrypt
import os

# Database configuration
DATABASE_URL = "sqlite:///job_dekho_streamlit.db"

# Create engine and base
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # 'student' or 'company'
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    student = relationship('Student', back_populates='user', uselist=False)
    company = relationship('Company', back_populates='user', uselist=False)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.email}>'


class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    roll_number = Column(String(20), unique=True, nullable=False)
    cgpa = Column(Float, nullable=False)
    branch = Column(String(100), nullable=False)
    skills = Column(Text)  # Comma-separated skills
    phone = Column(String(15))
    resume_path = Column(String(255))  # Path to uploaded resume
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='student')
    applications = relationship('Application', back_populates='student')
    
    def __repr__(self):
        return f'<Student {self.name}>'


class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    industry = Column(String(100))
    description = Column(Text)
    website = Column(String(200))
    contact_person = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='company')
    jobs = relationship('Job', back_populates='company')
    
    def __repr__(self):
        return f'<Company {self.name}>'


class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    min_cgpa = Column(Float, nullable=False)
    required_branch = Column(String(100), nullable=False)
    required_skills = Column(Text)  # Comma-separated skills
    salary = Column(String(50))
    location = Column(String(100))
    job_type = Column(String(20), default='Full-time')  # Full-time, Part-time, Internship
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship('Company', back_populates='jobs')
    applications = relationship('Application', back_populates='job')
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company.name if self.company else "Unknown"}>'


class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    status = Column(String(20), default='Applied')  # Applied, Shortlisted, Rejected, Selected
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite unique constraint to prevent duplicate applications
    __table_args__ = (UniqueConstraint('student_id', 'job_id', name='unique_student_job_application'),)
    
    # Relationships
    student = relationship('Student', back_populates='applications')
    job = relationship('Job', back_populates='applications')
    
    def __repr__(self):
        return f'<Application {self.student.name if self.student else "Unknown"} -> {self.job.title if self.job else "Unknown"}>'


def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables on import
if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")