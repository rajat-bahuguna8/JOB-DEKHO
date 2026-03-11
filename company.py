from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from functools import wraps
from database import db
from models import Company, Job, Application, Student
from sqlalchemy import desc
import os

company_bp = Blueprint('company', __name__)

def company_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'company':
            flash('Access denied', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@company_bp.route('/dashboard')
@login_required
@company_required
def dashboard():
    company = current_user.company
    jobs = Job.query.filter_by(company_id=company.id).all()
    
    total_applications = sum(len(job.applications) for job in jobs)
    active_jobs = sum(1 for job in jobs if job.is_active)
    
    all_applications = []
    for job in jobs:
        all_applications.extend(job.applications)
    
    stats = {
        'total_jobs': len(jobs),
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'shortlisted': sum(1 for app in all_applications if app.status == 'Shortlisted'),
        'interview': sum(1 for app in all_applications if app.status == 'Interview'),
        'selected': sum(1 for app in all_applications if app.status == 'Selected'),
        'pending': sum(1 for app in all_applications if app.status == 'Applied')
    }
    
    recent_applications = sorted(all_applications, key=lambda x: x.applied_at, reverse=True)[:10]
    
    return render_template('company/dashboard.html',
                         company=company,
                         jobs=jobs[:5],
                         stats=stats,
                         recent_applications=recent_applications)

@company_bp.route('/my-jobs')
@login_required
@company_required
def my_jobs():
    company = current_user.company
    jobs = Job.query.filter_by(company_id=company.id).order_by(desc(Job.created_at)).all()
    
    job_stats = {}
    for job in jobs:
        job_stats[job.id] = {
            'total': len(job.applications),
            'shortlisted': sum(1 for app in job.applications if app.status == 'Shortlisted'),
            'selected': sum(1 for app in job.applications if app.status == 'Selected')
        }
    
    return render_template('company/my_jobs.html', jobs=jobs, job_stats=job_stats)

@company_bp.route('/post-job', methods=['GET', 'POST'])
@login_required
@company_required
def post_job():
    if request.method == 'POST':
        job = Job(
            company_id=current_user.company.id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            min_cgpa=float(request.form.get('min_cgpa')),
            required_branch=request.form.get('required_branch'),
            required_skills=request.form.get('required_skills'),
            salary=request.form.get('salary'),
            location=request.form.get('location'),
            job_type=request.form.get('job_type'),
            is_active=True
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('company.my_jobs'))
    
    return render_template('company/post_job.html')

@company_bp.route('/job/<int:job_id>/applications')
@login_required
@company_required
def job_applications(job_id):
    job = Job.query.get_or_404(job_id)
    
    if job.company_id != current_user.company.id:
        flash('Access denied', 'danger')
        return redirect(url_for('company.my_jobs'))
    
    applications = sorted(job.applications, key=lambda x: x.match_score, reverse=True)
    
    return render_template('company/job_applications.html', job=job, applications=applications)

@company_bp.route('/application/<int:app_id>/update-status', methods=['POST'])
@login_required
@company_required
def update_application_status(app_id):
    application = Application.query.get_or_404(app_id)
    
    if application.job.company_id != current_user.company.id:
        flash('Access denied', 'danger')
        return redirect(url_for('company.dashboard'))
    
    new_status = request.form.get('status')
    if new_status in ['Applied', 'Shortlisted', 'Interview', 'Rejected', 'Selected']:
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}', 'success')
    
    return redirect(request.referrer or url_for('company.dashboard'))

@company_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@company_required
def profile():
    company = current_user.company
    
    if request.method == 'POST':
        company.name = request.form.get('name')
        company.industry = request.form.get('industry')
        company.description = request.form.get('description')
        company.website = request.form.get('website')
        company.contact_person = request.form.get('contact_person')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('company.profile'))
    
    return render_template('company/profile.html', company=company)

@company_bp.route('/view-resume/<int:student_id>')
@login_required
@company_required
def view_resume(student_id):
    """View/download student resume - only if student applied to company's job"""
    student = Student.query.get_or_404(student_id)
    company = current_user.company
    
    # Check if student has applied to any of this company's jobs
    has_applied = False
    for job in company.jobs:
        for app in job.applications:
            if app.student_id == student_id:
                has_applied = True
                break
        if has_applied:
            break
    
    if not has_applied:
        flash('You can only view resumes of students who applied to your jobs', 'danger')
        return redirect(url_for('company.dashboard'))
    
    if not student.resume_path:
        flash('Student has not uploaded a resume', 'warning')
        return redirect(request.referrer or url_for('company.dashboard'))
    
    # Send the resume file
    resume_directory = os.path.join(os.getcwd(), 'uploads', 'resumes')
    return send_from_directory(resume_directory, student.resume_path, as_attachment=False)
