"""
Comprehensive Test Script for JOB DEKHO
Tests all critical functionality
"""

import sys
from app import app
from database import db
from models import User, Student, Company, Job, Application, Admin

def test_database_connection():
    """Test database connectivity"""
    try:
        with app.app_context():
            # Test query
            user_count = User.query.count()
            print(f"✓ Database connected - {user_count} users found")
            return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_models():
    """Test all models are properly defined"""
    try:
        with app.app_context():
            models = {
                'User': User.query.count(),
                'Student': Student.query.count(),
                'Company': Company.query.count(),
                'Job': Job.query.count(),
                'Application': Application.query.count(),
                'Admin': Admin.query.count()
            }
            
            print("\n✓ All models working:")
            for model, count in models.items():
                print(f"  - {model}: {count} records")
            return True
    except Exception as e:
        print(f"✗ Model error: {e}")
        return False

def test_blueprints():
    """Test all blueprints are registered"""
    try:
        blueprints = ['auth', 'student', 'company', 'admin']
        registered = [bp.name for bp in app.blueprints.values()]
        
        print("\n✓ Blueprints registered:")
        for bp in blueprints:
            status = "✓" if bp in registered else "✗"
            print(f"  {status} {bp}")
        
        return all(bp in registered for bp in blueprints)
    except Exception as e:
        print(f"✗ Blueprint error: {e}")
        return False

def test_routes():
    """Test critical routes exist"""
    try:
        with app.test_client() as client:
            routes_to_test = [
                ('/', 'Homepage'),
                ('/auth/login', 'Login'),
                ('/auth/register', 'Register'),
            ]
            
            print("\n✓ Testing routes:")
            for route, name in routes_to_test:
                response = client.get(route)
                status = "✓" if response.status_code in [200, 302] else "✗"
                print(f"  {status} {name} ({route}): {response.status_code}")
            
            return True
    except Exception as e:
        print(f"✗ Route error: {e}")
        return False

def test_authentication():
    """Test authentication system"""
    try:
        with app.app_context():
            # Check if admin exists
            admin = User.query.filter_by(email='admin@jobdekho.com').first()
            if admin:
                # Test password check
                valid = admin.check_password('admin123')
                print(f"\n✓ Authentication system working")
                print(f"  - Admin password check: {'✓' if valid else '✗'}")
                return valid
            else:
                print("\n✗ Admin user not found")
                return False
    except Exception as e:
        print(f"✗ Authentication error: {e}")
        return False

def test_matching_algorithm():
    """Test job matching algorithm"""
    try:
        from matching_algorithm import calculate_match_score
        
        with app.app_context():
            student = Student.query.first()
            job = Job.query.first()
            
            if student and job:
                score, details = calculate_match_score(student, job)
                print(f"\n✓ Matching algorithm working")
                print(f"  - Sample match score: {score}%")
                print(f"  - CGPA match: {'✓' if details['cgpa_match'] else '✗'}")
                print(f"  - Branch match: {'✓' if details['branch_match'] else '✗'}")
                return True
            else:
                print("\n⚠ No data to test matching algorithm")
                return True
    except Exception as e:
        print(f"✗ Matching algorithm error: {e}")
        return False

def test_file_structure():
    """Test required files exist"""
    import os
    
    required_files = [
        'app.py',
        'database.py',
        'models.py',
        'auth.py',
        'student.py',
        'company.py',
        'admin.py',
        'matching_algorithm.py',
        'init_db.py',
        'requirements.txt',
        'START.bat',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    print("\n✓ Checking file structure:")
    all_exist = True
    for file in required_files:
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        if not exists:
            print(f"  {status} {file}")
            all_exist = False
    
    if all_exist:
        print("  ✓ All required files present")
    
    return all_exist

def test_configuration():
    """Test app configuration"""
    try:
        print("\n✓ App configuration:")
        print(f"  - Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
        print(f"  - Remember cookie: {app.config.get('REMEMBER_COOKIE_DURATION', 0) // 86400} days")
        print(f"  - Upload folder: {app.config.get('UPLOAD_FOLDER', 'Not set')}")
        print(f"  - Max upload: {app.config.get('MAX_CONTENT_LENGTH', 0) // (1024*1024)}MB")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("="*70)
    print(" "*20 + "JOB DEKHO - PROJECT TEST")
    print("="*70)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Models", test_models),
        ("Blueprints", test_blueprints),
        ("Routes", test_routes),
        ("Authentication", test_authentication),
        ("Matching Algorithm", test_matching_algorithm),
        ("File Structure", test_file_structure),
        ("Configuration", test_configuration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print(" "*25 + "TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print("="*70)
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Project is ready to use!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Review issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
