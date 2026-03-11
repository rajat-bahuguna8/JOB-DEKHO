#!/usr/bin/env python
"""
Job Dekho Streamlit Application - Startup Script
Run this script to start the Streamlit application with TTS functionality
"""

import subprocess
import sys
import os

def run_streamlit_app():
    """Run the Streamlit application"""
    
    print("=" * 60)
    print("      🏢 Job Dekho - Smart Job Portal with TTS")
    print("=" * 60)
    print("🚀 Starting Streamlit application...")
    print("📱 Features:")
    print("   • Student registration and job applications")
    print("   • Company registration and job posting")
    print("   • Intelligent matching algorithm") 
    print("   • 🔊 Text-to-Speech functionality")
    print("   • Voice-guided interface")
    print()
    print("🌐 The application will open in your default web browser")
    print("📍 Default URL: http://localhost:8501")
    print()
    print("⚠️  Note: Make sure your speakers are enabled for TTS functionality")
    print("🛑 Press Ctrl+C in this terminal to stop the server")
    print("=" * 60)
    
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Use the virtual environment python
        venv_python = os.path.join("job_dekho_env", "Scripts", "python.exe")
        streamlit_cmd = [venv_python, "-m", "streamlit", "run", "streamlit_app.py"]
        
        # Check if virtual environment exists
        if not os.path.exists(venv_python):
            print("❌ Virtual environment not found!")
            print("Please make sure the virtual environment 'job_dekho_env' exists.")
            return
        
        # Run streamlit
        print("🔄 Launching Streamlit...")
        subprocess.run(streamlit_cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        print("Thank you for using Job Dekho!")
    except Exception as e:
        print(f"\n❌ Error starting application: {str(e)}")
        print("Please check the installation and try again.")

if __name__ == "__main__":
    run_streamlit_app()