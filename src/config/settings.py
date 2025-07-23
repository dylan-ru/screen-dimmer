#!/usr/bin/env python3
"""
Settings Management

This module handles loading, saving, and managing application settings.
"""

import os
import json
from pathlib import Path

# Define the configuration directory and file
CONFIG_DIR = os.path.expanduser("~/.config/screen-dimmer")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def load_settings():
    """
    Load settings from the configuration file.
    
    Returns:
        dict: Application settings
    """
    # Default settings
    default_settings = {
        'dim_level': 0.3,
        'color': (0, 0, 0),
        'autostart': False,
        'monitors': {}
    }
    
    # Create config directory if it doesn't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # Try to load settings from file
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                settings = json.load(f)
                
                # Convert color from list to tuple if needed
                if 'color' in settings and isinstance(settings['color'], list):
                    settings['color'] = tuple(settings['color'])
                
                # Convert monitor colors from list to tuple if needed
                if 'monitors' in settings:
                    for monitor_id, monitor_settings in settings['monitors'].items():
                        if 'color' in monitor_settings and isinstance(monitor_settings['color'], list):
                            settings['monitors'][monitor_id]['color'] = tuple(monitor_settings['color'])
                
                return settings
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading settings: {e}")
    
    # Return default settings if loading fails
    return default_settings

def save_settings(settings):
    """
    Save settings to the configuration file.
    
    Args:
        settings (dict): Application settings to save
    """
    # Create config directory if it doesn't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # Convert color tuples to lists for JSON serialization
    settings_copy = settings.copy()
    
    if 'color' in settings_copy and isinstance(settings_copy['color'], tuple):
        settings_copy['color'] = list(settings_copy['color'])
    
    if 'monitors' in settings_copy:
        for monitor_id, monitor_settings in settings_copy['monitors'].items():
            if 'color' in monitor_settings and isinstance(monitor_settings['color'], tuple):
                settings_copy['monitors'][monitor_id]['color'] = list(monitor_settings['color'])
    
    # Save settings to file
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings_copy, f, indent=2)
    except IOError as e:
        print(f"Error saving settings: {e}")

def get_config_dir():
    """
    Get the configuration directory.
    
    Returns:
        str: Path to the configuration directory
    """
    return CONFIG_DIR

def get_config_file():
    """
    Get the configuration file path.
    
    Returns:
        str: Path to the configuration file
    """
    return CONFIG_FILE
