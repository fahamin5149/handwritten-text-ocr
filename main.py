"""
Image to Word Converter - Main Entry Point

A web application that converts images (JPG/PNG) into formatted Word documents (.docx)
using OCR technology with layout preservation.

Author: PPIT Project
Date: January 2026
"""

import sys
import os
import subprocess

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("Image to Word Converter - Streamlit Edition")
    print("=" * 60)
    print("Starting web application...")
    print()
    
    try:
        # Run the Streamlit app
        streamlit_app = os.path.join(project_root, "gui", "streamlit_app.py")
        subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_app])
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        print("\nTip: Make sure Streamlit is installed: pip install streamlit")
        sys.exit(1)


if __name__ == "__main__":
    main()
