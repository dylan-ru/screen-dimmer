#!/usr/bin/env python3
"""
Overlay Manager Implementation

This module manages multiple overlay windows for different displays.
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from src.overlay.overlay_window import OverlayWindow
from src.utils.display import get_monitors
from src.config.defaults import DEFAULT_COLOR

class OverlayManager:
    """
    Manages overlay windows for multiple displays.
    
    This class creates and manages overlay windows for each connected display,
    and handles display connection/disconnection events.
    """
    
    def __init__(self, settings):
        """
        Initialize the overlay manager.
        
        Args:
            settings (dict): Application settings including dim_level and color
        """
        self.settings = settings
        self.overlays = {}  # Dictionary of overlay windows by monitor ID
        
        # Get the default dim level and color from settings
        self.dim_level = settings.get('dim_level', 0.3)
        
        # Always use black as the color, regardless of settings
        self.color = DEFAULT_COLOR  # (0, 0, 0) - pure black
        
        # Get per-monitor settings if available
        self.monitor_settings = settings.get('monitors', {})
        
        # Ensure all monitor settings use black as the color
        for monitor_id in self.monitor_settings:
            if 'color' in self.monitor_settings[monitor_id]:
                self.monitor_settings[monitor_id]['color'] = DEFAULT_COLOR
        
        # Create overlay windows for all connected displays
        self.create_overlays()
        
        # Monitor display changes
        display = Gdk.Display.get_default()
        display.connect("monitor-added", self.on_monitor_added)
        display.connect("monitor-removed", self.on_monitor_removed)
    
    def create_overlays(self):
        """Create overlay windows for all connected displays."""
        # Get all connected monitors
        monitors = get_monitors()
        
        # Create an overlay window for each monitor
        for monitor in monitors:
            monitor_id = str(monitor.get_model())
            
            # Check if we have specific settings for this monitor
            monitor_dim_level = self.monitor_settings.get(monitor_id, {}).get('dim_level', self.dim_level)
            
            # Always use black as the color
            monitor_color = DEFAULT_COLOR
            
            # Create the overlay window
            overlay = OverlayWindow(
                display=monitor.get_display(),
                dim_level=monitor_dim_level,
                color=monitor_color
            )
            
            # Store the overlay
            self.overlays[monitor_id] = overlay
            
            # Position the overlay correctly for this monitor
            geometry = monitor.get_geometry()
            overlay.set_default_size(geometry.width, geometry.height - OverlayWindow.PANEL_HEIGHT)
            overlay.move(geometry.x, geometry.y + OverlayWindow.PANEL_HEIGHT)
    
    def show_all(self):
        """Show all overlay windows."""
        for overlay in self.overlays.values():
            overlay.show_all()
    
    def hide_all(self):
        """Hide all overlay windows."""
        for overlay in self.overlays.values():
            overlay.hide()
    
    def set_dim_level(self, level, monitor_id=None):
        """
        Set the dimming level for all or a specific overlay.
        
        Args:
            level (float): Dimming level from 0.0 (no dimming) to 1.0 (black)
            monitor_id (str, optional): Monitor ID to set the dim level for.
                If None, set for all monitors.
        """
        # Update the global dim level
        self.dim_level = level
        
        if monitor_id is None:
            # Update all overlays
            for overlay in self.overlays.values():
                overlay.set_dim_level(level)
            
            # Update settings
            self.settings['dim_level'] = level
        else:
            # Update specific overlay
            if monitor_id in self.overlays:
                self.overlays[monitor_id].set_dim_level(level)
                
                # Update monitor-specific settings
                if monitor_id not in self.monitor_settings:
                    self.monitor_settings[monitor_id] = {}
                self.monitor_settings[monitor_id]['dim_level'] = level
                self.settings['monitors'] = self.monitor_settings
    
    def set_color(self, color, monitor_id=None):
        """
        Set the overlay color for all or a specific overlay.
        
        Args:
            color (tuple): RGB color tuple (r, g, b) from 0 to 1
            monitor_id (str, optional): Monitor ID to set the color for.
                If None, set for all monitors.
        """
        # Update the global color (but always use black)
        self.color = DEFAULT_COLOR
        
        if monitor_id is None:
            # Update all overlays
            for overlay in self.overlays.values():
                overlay.set_color(DEFAULT_COLOR)
            
            # Update settings
            self.settings['color'] = DEFAULT_COLOR
        else:
            # Update specific overlay
            if monitor_id in self.overlays:
                self.overlays[monitor_id].set_color(DEFAULT_COLOR)
                
                # Update monitor-specific settings
                if monitor_id not in self.monitor_settings:
                    self.monitor_settings[monitor_id] = {}
                self.monitor_settings[monitor_id]['color'] = DEFAULT_COLOR
                self.settings['monitors'] = self.monitor_settings
    
    def get_settings(self):
        """
        Get the current settings.
        
        Returns:
            dict: Current settings including dim_level, color, and per-monitor settings
        """
        # Ensure color is always black before returning settings
        self.settings['color'] = DEFAULT_COLOR
        
        # Ensure all monitor settings use black as the color
        for monitor_id in self.monitor_settings:
            if 'color' in self.monitor_settings[monitor_id]:
                self.monitor_settings[monitor_id]['color'] = DEFAULT_COLOR
        
        self.settings['monitors'] = self.monitor_settings
        
        return self.settings
    
    def on_monitor_added(self, display, monitor):
        """
        Handle monitor connection event.
        
        Args:
            display (Gdk.Display): The display that changed
            monitor (Gdk.Monitor): The monitor that was added
        """
        monitor_id = str(monitor.get_model())
        
        # Check if we already have an overlay for this monitor
        if monitor_id in self.overlays:
            return
        
        # Check if we have specific settings for this monitor
        monitor_dim_level = self.monitor_settings.get(monitor_id, {}).get('dim_level', self.dim_level)
        
        # Always use black as the color
        monitor_color = DEFAULT_COLOR
        
        # Create the overlay window
        overlay = OverlayWindow(
            display=display,
            dim_level=monitor_dim_level,
            color=monitor_color
        )
        
        # Position the overlay correctly for this monitor
        geometry = monitor.get_geometry()
        overlay.set_default_size(geometry.width, geometry.height - OverlayWindow.PANEL_HEIGHT)
        overlay.move(geometry.x, geometry.y + OverlayWindow.PANEL_HEIGHT)
        
        # Store and show the overlay
        self.overlays[monitor_id] = overlay
        overlay.show_all()
    
    def on_monitor_removed(self, display, monitor):
        """
        Handle monitor disconnection event.
        
        Args:
            display (Gdk.Display): The display that changed
            monitor (Gdk.Monitor): The monitor that was removed
        """
        monitor_id = str(monitor.get_model())
        
        # Check if we have an overlay for this monitor
        if monitor_id in self.overlays:
            # Destroy the overlay
            self.overlays[monitor_id].destroy()
            del self.overlays[monitor_id]
