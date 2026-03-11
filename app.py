from flask import Flask, render_template, session
from database import db, login_manager
import os

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-2024')
    
    # Use SQLite database (easy setup, no MySQL required)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_dekho.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads/resumes'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}
    
    # Session configuration for persistent login
    app.config['REMEMBER_COOKIE_DURATION'] = 2592000  # 30 days in seconds
    app.config['REMEMBER_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['PERMANENT_SESSION_LIFETIME'] = 2592000  # 30 days
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    return app

app = create_app()

# Import models
from models import User, Student, Company, Job, Application, Admin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import blueprints
from auth import auth_bp
from student import student_bp
from company import company_bp
from admin import admin_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(company_bp, url_prefix='/company')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified successfully!")
    
    print("🚀 Starting Flask application...")
    print("📍 Access the application at: http://127.0.0.1:5000")
    print("⏹️  Press CTRL+C to stop the server")
    print()
    app.run(debug=True)
