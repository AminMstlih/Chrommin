# utils/installer.py
"""Installation utilities for Chrommin"""

import os
import sys
import subprocess
from pathlib import Path

def install_chrommin():
    """Install Chrommin and its dependencies"""
    print("🚀 Installing Chrommin...")
    
    # Check if Python is installed
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Python is not installed or not in PATH")
        print("Please install Python 3.8+ from https://python.org")
        return False
        
    # Create virtual environment
    venv_path = Path('venv')
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
    # Install dependencies
    pip_path = venv_path / 'Scripts' / 'pip.exe' if os.name == 'nt' else venv_path / 'bin' / 'pip'
    requirements_path = Path('requirements.txt')
    
    if requirements_path.exists():
        print("Installing dependencies...")
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        
    # Install Playwright browsers
    playwright_path = venv_path / 'Scripts' / 'playwright.exe' if os.name == 'nt' else venv_path / 'bin' / 'playwright'
    print("Installing browsers...")
    subprocess.run([str(playwright_path), "install", "chromium"], check=True)
    
    # Create necessary directories
    directories = ['profiles', 'extensions', 'config']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        
    print("✅ Chrommin installation complete!")
    print("💡 Next steps:")
    print("   1. Place browser extensions in the 'extensions' folder")
    print("   2. Run 'python main.py' to start Chrommin")
    print("   3. Use 'python main.py --gui' for graphical interface")
    
    return True