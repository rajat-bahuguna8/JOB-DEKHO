#!/usr/bin/env python
"""
Job Dekho - Job Portal Application
Run this script to start the development server
"""

from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("      Job Dekho - Job Portal Starting...")
    print("=" * 50)
    print(f"✓ Database: SQLite (job_dekho.db)")
    print(f"✓ Routes registered: {len([r for r in app.url_map.iter_rules()])}")
    print(f"✓ Templates: Available")
    print(f"✓ Static files: Available")
    print()
    print("🚀 Server starting at: http://127.0.0.1:5000")
    print("📖 Features:")
    print("   • Student registration and job applications")
    print("   • Company registration and job posting")
    print("   • Intelligent matching algorithm")
    print("   • Resume upload functionality")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        print("Thank you for using Job Dekho!")