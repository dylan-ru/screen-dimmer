#!/usr/bin/env python3
"""
Linux Screen Dimmer - Main Application Entry Point

This application creates a transparent overlay to dim the screen beyond
hardware brightness limits. It features system tray integration, multi-monitor
support, and persistent settings.
"""

import gi
import os
import sys
import signal

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import application modules
from src.overlay.overlay_manager import OverlayManager
from src.ui.tray import TrayIcon
from src.config.settings import load_settings, save_settings
from src.config.defaults import DEFAULT_COLOR

# Required GTK versions
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GLib

class LinuxScreenDimmer:
    """Main application class that coordinates all components."""
    
    def __init__(self):
        """Initialize the application."""
        # Load saved settings
        self.settings = load_settings()
        
        # Always set black as the default color, regardless of saved settings
        self.settings['color'] = DEFAULT_COLOR  # (0, 0, 0) - pure black
        
        # Create overlay manager
        self.overlay_manager = OverlayManager(self.settings)
        
        # Create system tray icon
        self.tray_icon = TrayIcon(self)
        
        # Setup signal handling for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def run(self):
        """Run the application main loop."""
        # Show the overlay windows
        self.overlay_manager.show_all()
        
        # Start the GTK main loop
        Gtk.main()
    
    def quit(self):
        """Quit the application."""
        # Save current settings
        save_settings(self.overlay_manager.get_settings())
        
        # Quit GTK main loop
        Gtk.main_quit()
    
    def signal_handler(self, sig, frame):
        """Handle system signals for clean shutdown."""
        self.quit()

def main():
    """Application entry point."""
    app = LinuxScreenDimmer()
    app.run()

if __name__ == "__main__":
    main()
