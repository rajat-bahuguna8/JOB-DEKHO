"""
Text-to-Speech utility functions for Job Dekho application
"""

import pyttsx3
import streamlit as st
import threading
import time


class TTSManager:
    """Text-to-Speech Manager"""
    
    def __init__(self):
        self.engine = None
        self.is_initialized = False
        self.is_speaking = False
    
    def initialize(self):
        """Initialize TTS engine"""
        try:
            self.engine = pyttsx3.init()
            
            # Set properties
            voices = self.engine.getProperty('voices')
            if voices:
                # Use first available voice
                self.engine.setProperty('voice', voices[0].id)
            
            # Set speech rate (words per minute)
            self.engine.setProperty('rate', 150)
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', 0.8)
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            st.error(f"Failed to initialize TTS engine: {str(e)}")
            return False
    
    def speak(self, text, blocking=False):
        """
        Convert text to speech
        Args:
            text (str): Text to speak
            blocking (bool): Whether to block until speech is complete
        """
        if not self.is_initialized:
            if not self.initialize():
                return False
        
        try:
            if self.is_speaking:
                return False
            
            self.is_speaking = True
            
            if blocking:
                self.engine.say(text)
                self.engine.runAndWait()
                self.is_speaking = False
            else:
                # Run in separate thread for non-blocking speech
                def speak_thread():
                    try:
                        self.engine.say(text)
                        self.engine.runAndWait()
                    finally:
                        self.is_speaking = False
                
                thread = threading.Thread(target=speak_thread)
                thread.daemon = True
                thread.start()
            
            return True
            
        except Exception as e:
            st.error(f"TTS Error: {str(e)}")
            self.is_speaking = False
            return False
    
    def stop(self):
        """Stop current speech"""
        try:
            if self.engine and self.is_speaking:
                self.engine.stop()
                self.is_speaking = False
                return True
        except Exception as e:
            st.error(f"Failed to stop TTS: {str(e)}")
        return False
    
    def is_available(self):
        """Check if TTS is available"""
        return self.is_initialized or self.initialize()


# Global TTS manager instance
tts_manager = TTSManager()


def speak_text(text, blocking=False):
    """
    Convenience function to speak text
    Args:
        text (str): Text to speak
        blocking (bool): Whether to block until speech is complete
    """
    return tts_manager.speak(text, blocking)


def stop_speech():
    """Stop current speech"""
    return tts_manager.stop()


def is_tts_available():
    """Check if TTS is available"""
    return tts_manager.is_available()


def create_tts_button(text, key=None, help_text=None):
    """
    Create a TTS button that speaks the given text
    Args:
        text (str): Text to speak
        key (str): Unique key for the button
        help_text (str): Help text for the button
    """
    if help_text is None:
        help_text = "Click to hear this text read aloud"
    
    if st.button("🔊 Listen", key=key, help=help_text):
        if text and text.strip():
            speak_text(text)
            st.success("🎵 Reading aloud...")
        else:
            st.warning("No text to read")


def add_tts_controls():
    """Add TTS controls to the sidebar"""
    with st.sidebar:
        st.subheader("🔊 Text-to-Speech")
        
        if is_tts_available():
            st.success("✅ TTS Available")
            
            if st.button("🛑 Stop Speech", key="stop_tts"):
                if stop_speech():
                    st.success("Speech stopped")
                else:
                    st.warning("No speech to stop")
        else:
            st.error("❌ TTS Not Available")
            st.caption("Text-to-speech functionality is not available on this system.")


def announce_page_title(title):
    """Announce the page title when page loads"""
    if 'last_announced_page' not in st.session_state:
        st.session_state.last_announced_page = None
    
    if st.session_state.last_announced_page != title:
        speak_text(f"Welcome to {title} page")
        st.session_state.last_announced_page = title


def announce_notification(message, message_type="info"):
    """
    Announce notifications with TTS
    Args:
        message (str): Message to announce
        message_type (str): Type of message (success, error, warning, info)
    """
    prefix = {
        'success': 'Success: ',
        'error': 'Error: ',
        'warning': 'Warning: ',
        'info': 'Information: '
    }.get(message_type, '')
    
    speak_text(prefix + message)


def create_job_card_with_tts(job, key_prefix=""):
    """
    Create a job card with TTS functionality
    Args:
        job: Job object with title, company, description, etc.
        key_prefix (str): Prefix for unique keys
    """
    with st.expander(f"🏢 {job.title} at {job.company.name if hasattr(job, 'company') and job.company else 'Unknown Company'}"):
        
        # Job details
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Description:** {job.description}")
            st.write(f"**Required CGPA:** {job.min_cgpa}+")
            st.write(f"**Branch:** {job.required_branch}")
            st.write(f"**Skills:** {job.required_skills}")
            if job.salary:
                st.write(f"**Salary:** {job.salary}")
            if job.location:
                st.write(f"**Location:** {job.location}")
        
        with col2:
            # TTS button for job details
            job_text = f"""
            Job title: {job.title}
            Company: {job.company.name if hasattr(job, 'company') and job.company else 'Unknown'}
            Description: {job.description}
            Required CGPA: {job.min_cgpa} or above
            Required Branch: {job.required_branch}
            Required Skills: {job.required_skills}
            """
            if job.salary:
                job_text += f"Salary: {job.salary}\n"
            if job.location:
                job_text += f"Location: {job.location}\n"
            
            create_tts_button(
                job_text.strip(), 
                key=f"{key_prefix}_job_tts_{job.id}",
                help_text="Listen to job details"
            )


# Test TTS functionality
def test_tts():
    """Test TTS functionality"""
    st.subheader("🔊 TTS Test")
    
    if is_tts_available():
        test_text = st.text_area("Enter text to test TTS:", value="Hello! This is a test of the text-to-speech functionality.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔊 Speak Text"):
                speak_text(test_text)
                st.success("Speaking...")
        
        with col2:
            if st.button("🛑 Stop"):
                stop_speech()
                st.success("Stopped")
    else:
        st.error("TTS not available. Please check your system configuration.")


if __name__ == "__main__":
    # Test the TTS functionality
    if is_tts_available():
        print("TTS is available!")
        speak_text("Hello! Text to speech is working correctly.", blocking=True)
    else:
        print("TTS is not available on this system.")