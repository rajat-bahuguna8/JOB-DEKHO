"""
Comprehensive File Generator for JOB DEKHO Project
Generates all HTML templates, CSS, and JavaScript files
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_file(path, content):
    """Create a file with given content"""
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created: {path}")

# BASE TEMPLATE
base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}JOB DEKHO - Find Your Dream Job{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-briefcase"></i> JOB DEKHO
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        {% if current_user.role == 'student' %}
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('student.dashboard') }}">Dashboard</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('student.browse_jobs') }}">Browse Jobs</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('student.my_applications') }}">My Applications</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('student.profile') }}">Profile</a>
                            </li>
                        {% elif current_user.role == 'company' %}
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('company.dashboard') }}">Dashboard</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('company.my_jobs') }}">My Jobs</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('company.post_job') }}">Post Job</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('company.profile') }}">Profile</a>
                            </li>
                        {% elif current_user.role == 'admin' %}
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('admin.dashboard') }}">Admin Dashboard</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('admin.manage_users') }}">Users</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('admin.analytics') }}">Analytics</a>
                            </li>
                        {% endif %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('auth.logout') }}">
                                <i class="fas fa-sign-out-alt"></i> Logout
                            </a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('auth.login') }}">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('auth.register') }}">Register</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <footer class="footer mt-5 py-3 bg-light">
        <div class="container text-center">
            <span class="text-muted">&copy; 2024 JOB DEKHO - All Rights Reserved</span>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''

# INDEX PAGE
index_html = '''{% extends "base.html" %}

{% block content %}
<div class="hero-section text-center py-5">
    <h1 class="display-3 fw-bold text-primary">Welcome to JOB DEKHO</h1>
    <p class="lead fs-4 text-muted">India's Smart Job Matching Platform</p>
    <p class="fs-5 mb-4">Find the perfect job match based on your CGPA, skills, and qualifications</p>
    
    <div class="row justify-content-center mt-5">
        <div class="col-md-5 mb-3">
            <div class="card h-100 shadow-sm hover-card">
                <div class="card-body text-center p-4">
                    <i class="fas fa-user-graduate fa-4x text-primary mb-3"></i>
                    <h3 class="card-title">For Students</h3>
                    <p class="card-text">Upload your resume and get matched with companies looking for candidates like you</p>
                    <a href="{{ url_for('auth.register') }}?role=student" class="btn btn-primary btn-lg">
                        <i class="fas fa-user-plus"></i> Register as Student
                    </a>
                </div>
            </div>
        </div>
        
        <div class="col-md-5 mb-3">
            <div class="card h-100 shadow-sm hover-card">
                <div class="card-body text-center p-4">
                    <i class="fas fa-building fa-4x text-success mb-3"></i>
                    <h3 class="card-title">For Companies</h3>
                    <p class="card-text">Post jobs and find the best candidates matched to your requirements</p>
                    <a href="{{ url_for('auth.register') }}?role=company" class="btn btn-success btn-lg">
                        <i class="fas fa-building"></i> Register as Company
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="features-section py-5">
    <h2 class="text-center mb-5">Why Choose JOB DEKHO?</h2>
    <div class="row">
        <div class="col-md-4 mb-4">
            <div class="feature-card text-center p-4">
                <i class="fas fa-robot fa-3x text-primary mb-3"></i>
                <h4>Smart Matching</h4>
                <p>AI-powered algorithm matches students with suitable jobs based on CGPA, skills, and branch</p>
            </div>
        </div>
        <div class="col-md-4 mb-4">
            <div class="feature-card text-center p-4">
                <i class="fas fa-clock fa-3x text-success mb-3"></i>
                <h4>Real-Time Tracking</h4>
                <p>Track your application status in real-time from submission to selection</p>
            </div>
        </div>
        <div class="col-md-4 mb-4">
            <div class="feature-card text-center p-4">
                <i class="fas fa-shield-alt fa-3x text-info mb-3"></i>
                <h4>Secure & Private</h4>
                <p>Your data is encrypted and secure. We respect your privacy</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

print("Starting file generation...")
print("="*60)

# Create base and index templates
create_file('templates/base.html', base_html)
create_file('templates/index.html', index_html)

print("\n✅ All basic templates created!")
print("\nNow run:")
print("  python create_auth_templates.py")
print("  python create_student_templates.py")
print("  python create_company_templates.py")
print("  python create_admin_templates.py")
print("  python create_static_files.py")
