#!/usr/bin/env python3
"""
Brightness Slider Component

This module provides a GTK slider widget for adjusting screen brightness.
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from src.config.defaults import MAX_DIM_LEVEL

class BrightnessSlider(Gtk.Scale):
    """
    A slider widget for adjusting screen brightness.
    
    This widget provides a horizontal slider that allows users to adjust
    the dimming level of the screen overlay.
    """
    
    def __init__(self, app):
        """
        Initialize the brightness slider.
        
        Args:
            app: The main application instance
        """
        # Create adjustment (0 to MAX_DIM_LEVEL)
        adjustment = Gtk.Adjustment(
            value=app.overlay_manager.dim_level,
            lower=0.0,
            upper=MAX_DIM_LEVEL,
            step_increment=0.01,
            page_increment=0.1,
            page_size=0
        )
        
        # Initialize the scale with the adjustment
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            adjustment=adjustment
        )
        
        self.app = app
        
        # Configure the slider
        self.set_size_request(200, -1)
        self.set_draw_value(False)
        self.set_value_pos(Gtk.PositionType.RIGHT)
        self.set_has_origin(True)
        self.set_show_fill_level(True)
        self.set_fill_level(MAX_DIM_LEVEL)
        self.set_restrict_to_fill_level(True)
        
        # Add marks
        self.add_mark(0.0, Gtk.PositionType.BOTTOM, "0%")
        self.add_mark(MAX_DIM_LEVEL / 2, Gtk.PositionType.BOTTOM, "50%")
        self.add_mark(MAX_DIM_LEVEL, Gtk.PositionType.BOTTOM, "100%")
        
        # Connect to value-changed signal
        self.connect("value-changed", self.on_value_changed)
        
        # Add a timeout to avoid too frequent updates
        self.timeout_id = None
    
    def on_value_changed(self, widget):
        """
        Handle slider value changes.
        
        Args:
            widget: The slider widget
        """
        # Get the current value
        value = widget.get_value()
        
        # Cancel any existing timeout
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
        
        # Set a timeout to update the overlay after a short delay
        self.timeout_id = GLib.timeout_add(50, self.update_overlay, value)
    
    def update_overlay(self, value):
        """
        Update the overlay dimming level.
        
        Args:
            value (float): The new dimming level
        
        Returns:
            bool: False to remove the timeout
        """
        # Update the overlay
        self.app.overlay_manager.set_dim_level(value)
        
        # Clear the timeout ID
        self.timeout_id = None
        
        return False
