"""
Job Dekho - Main Startup Script
Allows users to choose between Flask and Streamlit versions
"""

import sys
import os
import subprocess

def print_banner():
    print("=" * 60)
    print("🏢 JOB DEKHO - SMART JOB MATCHING PORTAL")
    print("=" * 60)
    print()

def show_menu():
    print("Choose which version you want to run:")
    print()
    print("1. Flask Web Application (Traditional web app)")
    print("   - Full-featured web interface")
    print("   - Runs on http://127.0.0.1:5000")
    print()
    print("2. Streamlit Application (Modern with TTS)")
    print("   - Interactive interface with Text-to-Speech")
    print("   - Voice-guided navigation")
    print("   - Runs on http://localhost:8501")
    print()
    print("3. Run Demo (Standalone demonstration)")
    print("   - See core features without web interface")
    print("   - Includes TTS demonstration")
    print()
    print("4. Exit")
    print()

def run_flask():
    print("\n🚀 Starting Flask application...")
    print("Access the application at: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n✅ Flask server stopped.")
    except Exception as e:
        print(f"\n❌ Error running Flask: {e}")

def run_streamlit():
    print("\n🚀 Starting Streamlit application...")
    print("The application will open in your browser automatically")
    print("If not, access it at: http://localhost:8501")
    print("Press CTRL+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n✅ Streamlit server stopped.")
    except Exception as e:
        print(f"\n❌ Error running Streamlit: {e}")

def run_demo():
    print("\n🚀 Running demonstration...")
    print()
    
    try:
        subprocess.run([sys.executable, "demo_job_dekho.py"], check=True)
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    missing = []
    
    # Core packages
    try:
        import flask
        print("✅ Flask installed")
    except ImportError:
        missing.append("Flask")
        print("❌ Flask not found")
    
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        missing.append("streamlit")
        print("❌ Streamlit not found")
    
    try:
        import pyttsx3
        print("✅ pyttsx3 (TTS) installed")
    except ImportError:
        missing.append("pyttsx3")
        print("❌ pyttsx3 not found")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\n📦 To install all dependencies, run:")
        print("   pip install -r requirements_complete.txt")
        print()
        
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    else:
        print("\n✅ All dependencies are installed!\n")
    
    return True

def main():
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies first.")
        return
    
    while True:
        show_menu()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            run_flask()
        elif choice == "2":
            run_streamlit()
        elif choice == "3":
            run_demo()
        elif choice == "4":
            print("\n👋 Thank you for using Job Dekho!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-4.\n")
        
        if choice in ["1", "2", "3"]:
            input("\nPress Enter to return to menu...")
            print("\n" * 2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
