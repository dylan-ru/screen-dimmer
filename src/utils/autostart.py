#!/usr/bin/env python3
"""
Autostart Functionality

This module provides functions for enabling/disabling application autostart.
"""

import os
import shutil
from pathlib import Path

from src.config.defaults import APP_NAME, APP_ID, APP_DESCRIPTION

# Define the autostart directory and file
AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
AUTOSTART_FILE = os.path.join(AUTOSTART_DIR, f"{APP_ID}.desktop")

def create_desktop_entry():
    """
    Create a desktop entry file for the application.
    
    Returns:
        str: The content of the desktop entry file
    """
    return f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Exec={APP_ID}
Icon=display-brightness-symbolic
Comment={APP_DESCRIPTION}
Categories=Utility;
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
"""

def is_autostart_enabled():
    """
    Check if autostart is enabled for the application.
    
    Returns:
        bool: True if autostart is enabled, False otherwise
    """
    return os.path.exists(AUTOSTART_FILE)

def enable_autostart():
    """
    Enable autostart for the application.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create autostart directory if it doesn't exist
        os.makedirs(AUTOSTART_DIR, exist_ok=True)
        
        # Create desktop entry file
        with open(AUTOSTART_FILE, 'w') as f:
            f.write(create_desktop_entry())
        
        return True
    except Exception as e:
        print(f"Error enabling autostart: {e}")
        return False

def disable_autostart():
    """
    Disable autostart for the application.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Remove desktop entry file if it exists
        if os.path.exists(AUTOSTART_FILE):
            os.remove(AUTOSTART_FILE)
        
        return True
    except Exception as e:
        print(f"Error disabling autostart: {e}")
        return False

def toggle_autostart(enabled):
    """
    Toggle autostart for the application.
    
    Args:
        enabled (bool): True to enable autostart, False to disable
    
    Returns:
        bool: True if successful, False otherwise
    """
    if enabled:
        return enable_autostart()
    else:
        return disable_autostart()

def create_application_desktop_entry(install_dir):
    """
    Create a desktop entry file for the application in the system applications directory.
    
    Args:
        install_dir (str): The installation directory
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Define the applications directory
        applications_dir = os.path.expanduser("~/.local/share/applications")
        desktop_file = os.path.join(applications_dir, f"{APP_ID}.desktop")
        
        # Create applications directory if it doesn't exist
        os.makedirs(applications_dir, exist_ok=True)
        
        # Create desktop entry content
        content = f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Exec={APP_ID}
Icon=display-brightness-symbolic
Comment={APP_DESCRIPTION}
Categories=Utility;
Terminal=false
StartupNotify=false
"""
        
        # Write desktop entry file
        with open(desktop_file, 'w') as f:
            f.write(content)
        
        # Make the file executable
        os.chmod(desktop_file, 0o755)
        
        return True
    except Exception as e:
        print(f"Error creating application desktop entry: {e}")
        return False
