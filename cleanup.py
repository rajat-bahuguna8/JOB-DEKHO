"""
Job Dekho - Cleanup Script
Removes unnecessary files and consolidates the project
"""

import os
import shutil

def remove_file(filepath):
    """Remove a file if it exists"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"✅ Removed: {filepath}")
            return True
        else:
            print(f"⚠️  Not found: {filepath}")
            return False
    except Exception as e:
        print(f"❌ Error removing {filepath}: {e}")
        return False

def remove_directory(dirpath):
    """Remove a directory if it exists"""
    try:
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
            print(f"✅ Removed directory: {dirpath}")
            return True
        else:
            print(f"⚠️  Not found: {dirpath}")
            return False
    except Exception as e:
        print(f"❌ Error removing {dirpath}: {e}")
        return False

def main():
    print("=" * 60)
    print("🧹 JOB DEKHO - CLEANUP SCRIPT")
    print("=" * 60)
    print("\nThis script will remove unnecessary files:")
    print("- Duplicate requirements files")
    print("- Old database files (keeping main ones)")
    print("- Unused batch scripts")
    print("- Python cache files")
    print()
    
    response = input("Do you want to continue? (y/n): ")
    if response.lower() != 'y':
        print("\n❌ Cleanup cancelled.")
        return
    
    print("\n🧹 Starting cleanup...\n")
    
    # Remove old requirements files (keep only requirements_complete.txt)
    files_to_remove = [
        "requirements.txt",  # Old Flask requirements
        "requirements_streamlit.txt",  # Old Streamlit requirements
        "start_job_dekho.bat",  # Old batch file
        "run_streamlit.py",  # Old runner
        "simple_streamlit_app.py",  # Old simple version
    ]
    
    for file in files_to_remove:
        remove_file(file)
    
    # Clean up Python cache
    print("\n🗑️  Cleaning Python cache files...")
    remove_directory("__pycache__")
    
    # Optionally remove old demo database
    print("\n💾 Checking database files...")
    if os.path.exists("job_dekho_demo.db"):
        response = input("\nRemove demo database (job_dekho_demo.db)? (y/n): ")
        if response.lower() == 'y':
            remove_file("job_dekho_demo.db")
    
    print("\n✅ Cleanup completed!")
    print("\n📁 Remaining important files:")
    print("   - start.py (main launcher)")
    print("   - requirements_complete.txt (all dependencies)")
    print("   - app.py (Flask version)")
    print("   - streamlit_app.py (Streamlit version)")
    print("   - demo_job_dekho.py (demo)")
    print("   - instance/job_dekho.db (Flask database)")
    print("   - job_dekho_streamlit.db (Streamlit database)")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cleanup cancelled.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
