#!/usr/bin/env python3
"""
Default Configuration

This module defines default configuration values for the application.
"""

# Default dimming level (0.0 to 1.0)
DEFAULT_DIM_LEVEL = 0.3

# Default overlay color (RGB tuple from 0 to 1)
DEFAULT_COLOR = (0, 0, 0)  # Black

# Default autostart setting
DEFAULT_AUTOSTART = False

# Maximum allowed dimming level to prevent complete blackout
MAX_DIM_LEVEL = 0.9

# Default configuration dictionary
DEFAULT_CONFIG = {
    'dim_level': DEFAULT_DIM_LEVEL,
    'color': DEFAULT_COLOR,
    'autostart': DEFAULT_AUTOSTART,
    'monitors': {}
}

# Application name
APP_NAME = "Screen Dimmer"

# Application ID (used for desktop entry, etc.)
APP_ID = "screen-dimmer"

# Application version
APP_VERSION = "1.0.0"

# Application author
APP_AUTHOR = "Screen Dimmer Team"

# Application website
APP_WEBSITE = "https://github.com/dylan-ru/screen-dimmer"

# Application description
APP_DESCRIPTION = "Reduce screen brightness beyond hardware limits"
