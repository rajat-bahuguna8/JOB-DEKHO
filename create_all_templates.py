"""Generate ALL remaining templates for JOB DEKHO"""
import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {path}")

base = "C:\\Users\\PC\\Desktop\\Job_Dekho"

# STUDENT TEMPLATES
templates = {
    f"{base}\\templates\\student\\browse_jobs.html": '''{% extends "base.html" %}
{% block title %}Browse Jobs{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-search"></i> Browse Jobs</h1>
<div class="filter-section mb-4">
    <form method="GET" class="row g-3">
        <div class="col-md-4">
            <input type="text" name="search" class="form-control" placeholder="Search jobs..." value="{{ search }}">
        </div>
        <div class="col-md-3">
            <select name="location" class="form-control">
                <option value="">All Locations</option>
                {% for loc in locations %}
                <option value="{{ loc }}" {% if location_filter == loc %}selected{% endif %}>{{ loc }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="col-md-3">
            <select name="job_type" class="form-control">
                <option value="">All Types</option>
                {% for jt in job_types %}
                <option value="{{ jt }}" {% if job_type_filter == jt %}selected{% endif %}>{{ jt }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100"><i class="fas fa-search"></i> Search</button>
        </div>
    </form>
</div>

{% for job, score, details in jobs_with_scores %}
<div class="card job-card mb-3">
    <div class="card-body">
        <div class="row">
            <div class="col-md-9">
                <h4>{{ job.title }}</h4>
                <h6 class="text-muted">{{ job.company.name }}</h6>
                <p>{{ job.description[:200] }}...</p>
                <p class="mb-1"><i class="fas fa-map-marker-alt"></i> {{ job.location }} | <i class="fas fa-briefcase"></i> {{ job.job_type }}</p>
                <p class="mb-1"><i class="fas fa-rupee-sign"></i> {{ job.salary }}</p>
                <p class="mb-0"><strong>Required:</strong> CGPA {{ job.min_cgpa }}+ | {{ job.required_branch }} | {{ job.required_skills }}</p>
            </div>
            <div class="col-md-3 text-center">
                <div class="match-score {% if score >= 85 %}high{% elif score >= 70 %}medium{% else %}low{% endif %}">
                    {{ score }}% Match
                </div>
                <div class="progress my-2">
                    <div class="progress-bar bg-{% if score >= 85 %}success{% elif score >= 70 %}warning{% else %}info{% endif %}" style="width: {{ score }}%"></div>
                </div>
                <form method="POST" action="{{ url_for('student.apply_job', job_id=job.id) }}">
                    <button type="submit" class="btn btn-primary btn-sm"><i class="fas fa-paper-plane"></i> Apply Now</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% else %}
<div class="alert alert-info">No matching jobs found.</div>
{% endfor %}
{% endblock %}''',

    f"{base}\\templates\\student\\my_applications.html": '''{% extends "base.html" %}
{% block title %}My Applications{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-file-alt"></i> My Applications</h1>
{% for app in applications %}
<div class="card mb-3">
    <div class="card-body">
        <div class="row">
            <div class="col-md-8">
                <h5>{{ app.job.title }}</h5>
                <p class="mb-1"><strong>{{ app.job.company.name }}</strong></p>
                <p class="mb-1">{{ app.job.location }} | {{ app.job.salary }}</p>
                <p class="text-muted mb-0">Applied: {{ app.applied_at.strftime('%d %b %Y, %I:%M %p') }}</p>
            </div>
            <div class="col-md-4 text-end">
                <h6>Match Score: {{ app.match_score }}%</h6>
                <span class="badge bg-{% if app.status == 'Selected' %}success{% elif app.status == 'Shortlisted' %}info{% elif app.status == 'Rejected' %}danger{% else %}warning{% endif %} fs-6">
                    {{ app.status }}
                </span>
            </div>
        </div>
    </div>
</div>
{% else %}
<div class="alert alert-info">You haven't applied to any jobs yet.</div>
{% endfor %}
{% endblock %}''',

    f"{base}\\templates\\student\\profile.html": '''{% extends "base.html" %}
{% block title %}My Profile{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-user"></i> My Profile</h1>
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-body">
                <form method="POST" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label class="form-label">Full Name</label>
                        <input type="text" name="name" class="form-control" value="{{ student.name }}" required>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Roll Number</label>
                            <input type="text" class="form-control" value="{{ student.roll_number }}" disabled>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">CGPA</label>
                            <input type="number" name="cgpa" step="0.01" class="form-control" value="{{ student.cgpa }}" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Branch</label>
                        <input type="text" name="branch" class="form-control" value="{{ student.branch }}" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Skills (comma-separated)</label>
                        <textarea name="skills" class="form-control" rows="3" required>{{ student.skills }}</textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Phone</label>
                        <input type="tel" name="phone" class="form-control" value="{{ student.phone }}">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Upload Resume (PDF/DOCX)</label>
                        <input type="file" name="resume" class="form-control" accept=".pdf,.doc,.docx">
                        {% if student.resume_path %}
                        <small class="text-muted">Current: {{ student.resume_path }}</small>
                        {% endif %}
                    </div>
                    <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Save Changes</button>
                </form>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body text-center">
                <i class="fas fa-user-circle fa-5x text-primary mb-3"></i>
                <h5>{{ student.name }}</h5>
                <p class="text-muted">{{ student.roll_number }}</p>
                <p><strong>CGPA:</strong> {{ student.cgpa }}</p>
                <p><strong>Branch:</strong> {{ student.branch }}</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    # COMPANY TEMPLATES
    f"{base}\\templates\\company\\dashboard.html": '''{% extends "base.html" %}
{% block title %}Company Dashboard{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-building"></i> {{ company.name }} Dashboard</h1>
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card stat-card bg-primary">
            <div class="card-body">
                <h5>Total Jobs</h5>
                <h2>{{ stats.total_jobs }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card stat-card bg-success">
            <div class="card-body">
                <h5>Active Jobs</h5>
                <h2>{{ stats.active_jobs }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card stat-card bg-info">
            <div class="card-body">
                <h5>Applications</h5>
                <h2>{{ stats.total_applications }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card stat-card bg-warning">
            <div class="card-body">
                <h5>Selected</h5>
                <h2>{{ stats.selected }}</h2>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <h3>Recent Job Postings</h3>
        {% for job in jobs %}
        <div class="card mb-2">
            <div class="card-body">
                <h6>{{ job.title }}</h6>
                <p class="mb-0 small text-muted">{{ job.location }} | {{ len(job.applications) }} applications</p>
            </div>
        </div>
        {% endfor %}
        <a href="{{ url_for('company.my_jobs') }}" class="btn btn-primary">View All Jobs</a>
    </div>
    <div class="col-md-6">
        <h3>Recent Applications</h3>
        {% for app in recent_applications %}
        <div class="card mb-2">
            <div class="card-body">
                <h6>{{ app.student.name }} - {{ app.job.title }}</h6>
                <p class="mb-0"><span class="badge bg-{{ 'success' if app.status == 'Selected' else 'info' if app.status == 'Shortlisted' else 'warning' }}">{{ app.status }}</span> | Match: {{ app.match_score }}%</p>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    f"{base}\\templates\\company\\my_jobs.html": '''{% extends "base.html" %}
{% block title %}My Jobs{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-briefcase"></i> My Job Postings</h1>
<a href="{{ url_for('company.post_job') }}" class="btn btn-success mb-3"><i class="fas fa-plus"></i> Post New Job</a>

{% for job in jobs %}
<div class="card mb-3">
    <div class="card-body">
        <div class="row">
            <div class="col-md-8">
                <h5>{{ job.title }} {% if not job.is_active %}<span class="badge bg-secondary">Inactive</span>{% endif %}</h5>
                <p>{{ job.description[:150] }}...</p>
                <p class="mb-1"><strong>Requirements:</strong> CGPA {{ job.min_cgpa }}+ | {{ job.required_branch }}</p>
                <p class="text-muted mb-0">Posted: {{ job.created_at.strftime('%d %b %Y') }}</p>
            </div>
            <div class="col-md-4">
                <p><strong>Applications:</strong> {{ job_stats[job.id].total }}</p>
                <p><strong>Shortlisted:</strong> {{ job_stats[job.id].shortlisted }}</p>
                <p><strong>Selected:</strong> {{ job_stats[job.id].selected }}</p>
                <a href="{{ url_for('company.job_applications', job_id=job.id) }}" class="btn btn-primary btn-sm">View Applications</a>
            </div>
        </div>
    </div>
</div>
{% endfor %}
{% endblock %}''',

    f"{base}\\templates\\company\\post_job.html": '''{% extends "base.html" %}
{% block title %}Post Job{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-plus-circle"></i> Post New Job</h1>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">Job Title</label>
                <input type="text" name="title" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea name="description" class="form-control" rows="4" required></textarea>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">Minimum CGPA</label>
                    <input type="number" name="min_cgpa" step="0.1" min="0" max="10" class="form-control" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Required Branch</label>
                    <input type="text" name="required_branch" class="form-control" placeholder="e.g., Computer Science" required>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Required Skills (comma-separated)</label>
                <textarea name="required_skills" class="form-control" rows="2" placeholder="e.g., Python, Java, SQL" required></textarea>
            </div>
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label class="form-label">Salary</label>
                    <input type="text" name="salary" class="form-control" placeholder="e.g., ₹5-7 LPA" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label class="form-label">Location</label>
                    <input type="text" name="location" class="form-control" required>
                </div>
                <div class="col-md-4 mb-3">
                    <label class="form-label">Job Type</label>
                    <select name="job_type" class="form-control" required>
                        <option value="Full-time">Full-time</option>
                        <option value="Part-time">Part-time</option>
                        <option value="Internship">Internship</option>
                    </select>
                </div>
            </div>
            <button type="submit" class="btn btn-success"><i class="fas fa-check"></i> Post Job</button>
            <a href="{{ url_for('company.my_jobs') }}" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</div>
{% endblock %}''',

    f"{base}\\templates\\company\\job_applications.html": '''{% extends "base.html" %}
{% block title %}Applications for {{ job.title }}{% endblock %}
{% block content %}
<h1 class="mb-4">Applications for: {{ job.title }}</h1>
<p class="lead">{{ applications|length }} candidates applied</p>

{% for app in applications %}
<div class="card mb-3">
    <div class="card-body">
        <div class="row">
            <div class="col-md-7">
                <h5>{{ app.student.name }}</h5>
                <p class="mb-1"><strong>CGPA:</strong> {{ app.student.cgpa }} | <strong>Branch:</strong> {{ app.student.branch }}</p>
                <p class="mb-1"><strong>Skills:</strong> {{ app.student.skills }}</p>
                <p class="mb-0 text-muted">Applied: {{ app.applied_at.strftime('%d %b %Y') }}</p>
            </div>
            <div class="col-md-3">
                <h6>Match Score</h6>
                <div class="progress mb-2">
                    <div class="progress-bar bg-{% if app.match_score >= 85 %}success{% elif app.match_score >= 70 %}warning{% else %}info{% endif %}" style="width: {{ app.match_score }}%">{{ app.match_score }}%</div>
                </div>
                <span class="badge bg-{{ 'success' if app.status == 'Selected' else 'info' if app.status == 'Shortlisted' else 'danger' if app.status == 'Rejected' else 'warning' }}">{{ app.status }}</span>
            </div>
            <div class="col-md-2">
                <form method="POST" action="{{ url_for('company.update_application_status', app_id=app.id) }}">
                    <select name="status" class="form-control mb-2">
                        <option value="Applied" {% if app.status == 'Applied' %}selected{% endif %}>Applied</option>
                        <option value="Shortlisted" {% if app.status == 'Shortlisted' %}selected{% endif %}>Shortlisted</option>
                        <option value="Selected" {% if app.status == 'Selected' %}selected{% endif %}>Selected</option>
                        <option value="Rejected" {% if app.status == 'Rejected' %}selected{% endif %}>Rejected</option>
                    </select>
                    <button type="submit" class="btn btn-sm btn-primary">Update</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endfor %}
{% endblock %}''',

    f"{base}\\templates\\company\\profile.html": '''{% extends "base.html" %}
{% block title %}Company Profile{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-building"></i> Company Profile</h1>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">Company Name</label>
                <input type="text" name="name" class="form-control" value="{{ company.name }}" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Industry</label>
                <input type="text" name="industry" class="form-control" value="{{ company.industry }}">
            </div>
            <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea name="description" class="form-control" rows="4">{{ company.description }}</textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">Website</label>
                <input type="url" name="website" class="form-control" value="{{ company.website }}">
            </div>
            <div class="mb-3">
                <label class="form-label">Contact Person</label>
                <input type="text" name="contact_person" class="form-control" value="{{ company.contact_person }}">
            </div>
            <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Save Changes</button>
        </form>
    </div>
</div>
{% endblock %}''',

    # ADMIN TEMPLATES
    f"{base}\\templates\\admin\\dashboard.html": '''{% extends "base.html" %}
{% block title %}Admin Dashboard{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-tachometer-alt"></i> Admin Dashboard</h1>
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card admin-card">
            <div class="card-body">
                <h6 class="text-muted">Total Students</h6>
                <div class="metric-number">{{ total_students }}</div>
                <small class="text-success">+{{ new_students }} this week</small>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card admin-card">
            <div class="card-body">
                <h6 class="text-muted">Total Companies</h6>
                <div class="metric-number">{{ total_companies }}</div>
                <small class="text-success">+{{ new_companies }} this week</small>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card admin-card">
            <div class="card-body">
                <h6 class="text-muted">Total Jobs</h6>
                <div class="metric-number">{{ total_jobs }}</div>
                <small>{{ active_jobs }} active</small>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card admin-card">
            <div class="card-body">
                <h6 class="text-muted">Applications</h6>
                <div class="metric-number">{{ total_applications }}</div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <h4>Application Status Breakdown</h4>
        <div class="card">
            <div class="card-body">
                {% for status, count in status_breakdown.items() %}
                <p><strong>{{ status }}:</strong> {{ count }}</p>
                {% endfor %}
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <h4>Top Companies by Jobs</h4>
        <div class="card">
            <div class="card-body">
                {% for company_name, job_count in top_companies %}
                <p><strong>{{ company_name }}:</strong> {{ job_count }} jobs</p>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    f"{base}\\templates\\admin\\users.html": '''{% extends "base.html" %}
{% block title %}User Management{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-users"></i> User Management</h1>
<div class="filter-section mb-3">
    <form method="GET" class="row g-3">
        <div class="col-md-4">
            <input type="text" name="search" class="form-control" placeholder="Search by email..." value="{{ search }}">
        </div>
        <div class="col-md-3">
            <select name="role" class="form-control">
                <option value="">All Roles</option>
                <option value="student" {% if role_filter == 'student' %}selected{% endif %}>Students</option>
                <option value="company" {% if role_filter == 'company' %}selected{% endif %}>Companies</option>
            </select>
        </div>
        <div class="col-md-3">
            <select name="status" class="form-control">
                <option value="">All Status</option>
                <option value="active" {% if status_filter == 'active' %}selected{% endif %}>Active</option>
                <option value="inactive" {% if status_filter == 'inactive' %}selected{% endif %}>Inactive</option>
            </select>
        </div>
        <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100">Filter</button>
        </div>
    </form>
</div>

<table class="table table-hover">
    <thead>
        <tr>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Created</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
        <tr>
            <td>{{ user.email }}</td>
            <td><span class="badge bg-{% if user.role == 'student' %}primary{% elif user.role == 'company' %}success{% else %}danger{% endif %}">{{ user.role }}</span></td>
            <td><span class="badge bg-{% if user.is_active %}success{% else %}secondary{% endif %}">{% if user.is_active %}Active{% else %}Inactive{% endif %}</span></td>
            <td>{{ user.created_at.strftime('%d %b %Y') }}</td>
            <td>
                {% if user.role != 'admin' %}
                <form method="POST" action="{{ url_for('admin.toggle_user_status', user_id=user.id) }}" style="display:inline">
                    <button type="submit" class="btn btn-sm btn-warning">Toggle</button>
                </form>
                <form method="POST" action="{{ url_for('admin.delete_user', user_id=user.id) }}" style="display:inline" onsubmit="return confirm('Delete this user?')">
                    <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                </form>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

    f"{base}\\templates\\admin\\analytics.html": '''{% extends "base.html" %}
{% block title %}Analytics{% endblock %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-chart-line"></i> Platform Analytics</h1>
<div class="row mb-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-body">
                <h5>Success Rate</h5>
                <h2 class="text-success">{{ success_rate }}%</h2>
                <p class="text-muted">Of total applications</p>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-body">
                <h5>Average CGPA of Selected Candidates</h5>
                <h2 class="text-primary">{{ avg_cgpa }}</h2>
            </div>
        </div>
    </div>
</div>

<div class="card">
    <div class="card-body">
        <h5>Top 10 In-Demand Skills</h5>
        {% for skill, count in top_skills %}
        <div class="mb-2">
            <strong>{{ skill.title() }}</strong>
            <div class="progress">
                <div class="progress-bar" style="width: {{ (count / top_skills[0][1] * 100) }}%">{{ count }} jobs</div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',
}

print("Creating ALL templates...")
for path, content in templates.items():
    create_file(path, content)

print(f"\n✅ Created {len(templates)} template files!")
print("\n🎉 ALL TEMPLATES COMPLETE!")
print("\nYou can now run:")
print("  1. python init_db.py")
print("  2. python app.py")
print("  3. Open http://127.0.0.1:5000")
