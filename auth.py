from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from database import db
from models import User, Student, Company, Admin
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        elif current_user.role == 'company':
            return redirect(url_for('company.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Contact admin.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Remember me functionality
            remember = request.form.get('remember', False)
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'Welcome back!', 'success')
            
            if user.role == 'student':
                return redirect(url_for('student.dashboard'))
            elif user.role == 'company':
                return redirect(url_for('company.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    role = request.args.get('role', 'student')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(email=email, role=role, is_active=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        
        if role == 'student':
            student = Student(
                user_id=user.id,
                name=request.form.get('name'),
                roll_number=request.form.get('roll_number'),
                cgpa=float(request.form.get('cgpa')),
                branch=request.form.get('branch'),
                skills=request.form.get('skills'),
                phone=request.form.get('phone')
            )
            db.session.add(student)
        elif role == 'company':
            company = Company(
                user_id=user.id,
                name=request.form.get('name'),
                industry=request.form.get('industry'),
                description=request.form.get('description'),
                website=request.form.get('website'),
                contact_person=request.form.get('contact_person')
            )
            db.session.add(company)
        
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', role=role)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
