from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from database import db
from models import Student, Job, Application
from matching_algorithm import calculate_match_score, get_recommended_jobs, auto_shortlist_status
import os

student_bp = Blueprint('student', __name__)

def student_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('Access denied', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    student = current_user.student
    
    # Check if resume uploaded
    if not student.resume_path:
        flash('Please upload your resume to view job recommendations', 'warning')
        return redirect(url_for('student.profile'))
    
    applications = Application.query.filter_by(student_id=student.id).all()
    
    stats = {
        'total_applications': len(applications),
        'shortlisted': sum(1 for app in applications if app.status == 'Shortlisted'),
        'interview': sum(1 for app in applications if app.status == 'Interview'),
        'selected': sum(1 for app in applications if app.status == 'Selected'),
        'rejected': sum(1 for app in applications if app.status == 'Rejected'),
        'pending': sum(1 for app in applications if app.status == 'Applied')
    }
    
    # Get recommended jobs
    all_jobs = Job.query.filter_by(is_active=True).all()
    recommendations = get_recommended_jobs(student, all_jobs, min_match_score=60)[:5]
    
    return render_template('student/dashboard.html', 
                         student=student,
                         applications=applications[:5],
                         stats=stats,
                         recommendations=recommendations)

@student_bp.route('/browse-jobs')
@login_required
@student_required
def browse_jobs():
    student = current_user.student
    
    # Check if resume uploaded - REQUIRED to view jobs
    if not student.resume_path:
        flash('Please upload your resume first to browse jobs', 'warning')
        return redirect(url_for('student.profile'))
    
    # Search and filters
    search = request.args.get('search', '')
    location_filter = request.args.get('location', '')
    job_type_filter = request.args.get('job_type', '')
    
    query = Job.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(Job.title.contains(search) | Job.description.contains(search))
    if location_filter:
        query = query.filter_by(location=location_filter)
    if job_type_filter:
        query = query.filter_by(job_type=job_type_filter)
    
    all_jobs = query.all()
    
    # Calculate match scores
    jobs_with_scores = []
    for job in all_jobs:
        score, details = calculate_match_score(student, job)
        if score > 0:  # Only show jobs that match
            jobs_with_scores.append((job, score, details))
    
    jobs_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Get locations and job types for filters
    locations = db.session.query(Job.location).distinct().all()
    job_types = db.session.query(Job.job_type).distinct().all()
    
    return render_template('student/browse_jobs.html',
                         jobs_with_scores=jobs_with_scores,
                         locations=[l[0] for l in locations],
                         job_types=[jt[0] for jt in job_types],
                         search=search,
                         location_filter=location_filter,
                         job_type_filter=job_type_filter)

@student_bp.route('/apply/<int:job_id>', methods=['POST'])
@login_required
@student_required
def apply_job(job_id):
    student = current_user.student
    
    # Check if resume uploaded
    if not student.resume_path:
        flash('Please upload your resume before applying', 'danger')
        return redirect(url_for('student.profile'))
    
    job = Job.query.get_or_404(job_id)
    
    # Check if already applied
    existing = Application.query.filter_by(student_id=student.id, job_id=job_id).first()
    if existing:
        flash('You have already applied to this job', 'warning')
        return redirect(url_for('student.browse_jobs'))
    
    # Calculate match score
    score, details = calculate_match_score(student, job)
    
    if score == 0:
        flash('You do not meet the requirements for this job', 'danger')
        return redirect(url_for('student.browse_jobs'))
    
    # Determine initial status
    status = auto_shortlist_status(score)
    
    application = Application(
        student_id=student.id,
        job_id=job_id,
        status=status,
        match_score=score
    )
    db.session.add(application)
    db.session.commit()
    
    flash(f'Application submitted successfully! Match Score: {score}%', 'success')
    return redirect(url_for('student.my_applications'))

@student_bp.route('/my-applications')
@login_required
@student_required
def my_applications():
    student = current_user.student
    applications = Application.query.filter_by(student_id=student.id).order_by(Application.applied_at.desc()).all()
    
    return render_template('student/my_applications.html', applications=applications)

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@student_required
def profile():
    student = current_user.student
    
    if request.method == 'POST':
        student.name = request.form.get('name')
        student.phone = request.form.get('phone')
        student.cgpa = float(request.form.get('cgpa'))
        student.branch = request.form.get('branch')
        student.skills = request.form.get('skills')
        
        # Handle resume upload
        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename:
                filename = secure_filename(f"{student.roll_number}_{file.filename}")
                file.save(os.path.join('uploads/resumes', filename))
                student.resume_path = filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.profile'))
    
    return render_template('student/profile.html', student=student)
