from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from database import db
from models import User, Student, Company, Job, Application, Admin
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()
    active_jobs = Job.query.filter_by(is_active=True).count()
    
    # Application status breakdown
    status_breakdown = db.session.query(
        Application.status,
        func.count(Application.id)
    ).group_by(Application.status).all()
    
    # Recent applications (last 10)
    recent_applications = Application.query.order_by(
        desc(Application.applied_at)
    ).limit(10).all()
    
    # Top companies by job postings
    top_companies = db.session.query(
        Company.name,
        func.count(Job.id).label('job_count')
    ).join(Job).group_by(Company.id).order_by(desc('job_count')).limit(5).all()
    
    # Students by branch
    students_by_branch = db.session.query(
        Student.branch,
        func.count(Student.id)
    ).group_by(Student.branch).all()
    
    # Recent registrations (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_students = Student.query.filter(Student.created_at >= week_ago).count()
    new_companies = Company.query.filter(Company.created_at >= week_ago).count()
    
    return render_template('admin/dashboard.html',
                         total_students=total_students,
                         total_companies=total_companies,
                         total_jobs=total_jobs,
                         total_applications=total_applications,
                         active_jobs=active_jobs,
                         status_breakdown=dict(status_breakdown),
                         recent_applications=recent_applications,
                         top_companies=top_companies,
                         students_by_branch=dict(students_by_branch),
                         new_students=new_students,
                         new_companies=new_companies)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    # Search and filter
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    status_filter = request.args.get('status', '')
    
    query = User.query
    
    if search:
        query = query.filter(User.email.contains(search))
    if role_filter:
        query = query.filter_by(role=role_filter)
    if status_filter == 'active':
        query = query.filter_by(is_active=True)
    elif status_filter == 'inactive':
        query = query.filter_by(is_active=False)
    
    users = query.order_by(desc(User.created_at)).all()
    
    return render_template('admin/users.html', 
                         users=users,
                         search=search,
                         role_filter=role_filter,
                         status_filter=status_filter)

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.role == 'admin':
        flash('Cannot modify admin user status.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.email} has been {status}.', 'success')
    
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.role == 'admin':
        flash('Cannot delete admin user.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    email = user.email
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {email} has been deleted.', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/companies')
@login_required
@admin_required
def manage_companies():
    search = request.args.get('search', '')
    
    query = Company.query
    if search:
        query = query.filter(Company.name.contains(search))
    
    companies = query.order_by(desc(Company.created_at)).all()
    
    # Get job counts for each company
    company_stats = {}
    for company in companies:
        company_stats[company.id] = {
            'total_jobs': len(company.jobs),
            'active_jobs': sum(1 for job in company.jobs if job.is_active),
            'total_applications': sum(len(job.applications) for job in company.jobs)
        }
    
    return render_template('admin/companies.html',
                         companies=companies,
                         company_stats=company_stats,
                         search=search)

@admin_bp.route('/students')
@login_required
@admin_required
def manage_students():
    search = request.args.get('search', '')
    branch_filter = request.args.get('branch', '')
    
    query = Student.query
    
    if search:
        query = query.filter(
            db.or_(
                Student.name.contains(search),
                Student.roll_number.contains(search)
            )
        )
    if branch_filter:
        query = query.filter_by(branch=branch_filter)
    
    students = query.order_by(desc(Student.created_at)).all()
    
    # Get unique branches for filter
    branches = db.session.query(Student.branch).distinct().all()
    branches = [b[0] for b in branches]
    
    return render_template('admin/students.html',
                         students=students,
                         branches=branches,
                         search=search,
                         branch_filter=branch_filter)

@admin_bp.route('/jobs')
@login_required
@admin_required
def manage_jobs():
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    query = Job.query
    
    if search:
        query = query.filter(Job.title.contains(search))
    if status_filter == 'active':
        query = query.filter_by(is_active=True)
    elif status_filter == 'inactive':
        query = query.filter_by(is_active=False)
    
    jobs = query.order_by(desc(Job.created_at)).all()
    
    return render_template('admin/jobs.html',
                         jobs=jobs,
                         search=search,
                         status_filter=status_filter)

@admin_bp.route('/jobs/<int:job_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_job_status(job_id):
    job = Job.query.get_or_404(job_id)
    job.is_active = not job.is_active
    db.session.commit()
    
    status = 'activated' if job.is_active else 'deactivated'
    flash(f'Job "{job.title}" has been {status}.', 'success')
    
    return redirect(url_for('admin.manage_jobs'))

@admin_bp.route('/applications')
@login_required
@admin_required
def manage_applications():
    status_filter = request.args.get('status', '')
    
    query = Application.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    applications = query.order_by(desc(Application.applied_at)).all()
    
    return render_template('admin/applications.html',
                         applications=applications,
                         status_filter=status_filter)

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    # Time-based analytics
    days = int(request.args.get('days', 30))
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Applications over time
    applications_by_day = db.session.query(
        func.date(Application.applied_at).label('date'),
        func.count(Application.id).label('count')
    ).filter(Application.applied_at >= start_date).group_by(
        func.date(Application.applied_at)
    ).all()
    
    # Jobs posted over time
    jobs_by_day = db.session.query(
        func.date(Job.created_at).label('date'),
        func.count(Job.id).label('count')
    ).filter(Job.created_at >= start_date).group_by(
        func.date(Job.created_at)
    ).all()
    
    # Success rate (Selected / Total Applications)
    total_apps = Application.query.count()
    selected_apps = Application.query.filter_by(status='Selected').count()
    success_rate = (selected_apps / total_apps * 100) if total_apps > 0 else 0
    
    # Average CGPA of successful candidates
    avg_cgpa = db.session.query(func.avg(Student.cgpa)).join(
        Application
    ).filter(Application.status == 'Selected').scalar() or 0
    
    # Most in-demand skills
    all_jobs = Job.query.filter_by(is_active=True).all()
    skills_count = {}
    for job in all_jobs:
        if job.required_skills:
            skills = [s.strip().lower() for s in job.required_skills.split(',')]
            for skill in skills:
                skills_count[skill] = skills_count.get(skill, 0) + 1
    
    top_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return render_template('admin/analytics.html',
                         applications_by_day=applications_by_day,
                         jobs_by_day=jobs_by_day,
                         success_rate=round(success_rate, 2),
                         avg_cgpa=round(avg_cgpa, 2),
                         top_skills=top_skills,
                         days=days)

@admin_bp.route('/api/stats')
@login_required
@admin_required
def api_stats():
    """API endpoint for real-time dashboard updates"""
    stats = {
        'total_students': Student.query.count(),
        'total_companies': Company.query.count(),
        'total_jobs': Job.query.count(),
        'total_applications': Application.query.count(),
        'active_jobs': Job.query.filter_by(is_active=True).count(),
        'pending_applications': Application.query.filter_by(status='Applied').count(),
        'timestamp': datetime.utcnow().isoformat()
    }
    return jsonify(stats)
