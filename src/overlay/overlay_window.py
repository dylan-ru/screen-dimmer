#!/usr/bin/env python3
"""
Overlay Window Implementation

This module provides the transparent overlay window that dims the screen.
"""

import gi
import cairo

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkX11

class OverlayWindow(Gtk.Window):
    """
    A transparent overlay window that dims the screen.
    
    This window sits on top of all other windows and has click-through capability
    so that users can interact with windows beneath it.
    """
    
    # Panel height in pixels (space to leave at the top of the screen)
    PANEL_HEIGHT = 30
    
    def __init__(self, display=None, dim_level=0.5, color=(0, 0, 0)):
        """
        Initialize the overlay window.
        
        Args:
            display (Gdk.Display, optional): The display to create the window on.
                If None, the default display is used.
            dim_level (float): The dimming level from 0.0 (no dimming) to 1.0 (black).
            color (tuple): RGB color tuple for the overlay (r, g, b) from 0 to 1.
        """
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        
        # Store parameters
        self.dim_level = dim_level
        self.color = color
        self.display = display or Gdk.Display.get_default()
        self.monitor = self.display.get_primary_monitor()
        
        # Configure window properties
        self.set_title("Screen Dimmer Overlay")
        self.set_keep_above(True)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_accept_focus(False)
        self.set_app_paintable(True)
        
        # Get monitor geometry
        geometry = self.monitor.get_geometry()
        
        # Set window size to cover the screen except for the panel area
        self.set_default_size(geometry.width, geometry.height - self.PANEL_HEIGHT)
        self.move(geometry.x, geometry.y + self.PANEL_HEIGHT)
        
        # Make window click-through
        self.set_events(0)  # No events
        
        # Set up visual for transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual is not None and screen.is_composited():
            self.set_visual(visual)
        else:
            print("Warning: Screen does not support alpha channels!")
            # Fall back to RGB visual
            self.set_visual(screen.get_system_visual())
        
        # Create drawing area for the overlay
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_draw)
        self.add(self.drawing_area)
        
        # Connect to window events
        self.connect("delete-event", self.on_delete_event)
        
        # Make input transparent (click-through)
        self.set_input_shape()
    
    def on_draw(self, widget, cr):
        """
        Draw the overlay with the specified color and opacity.
        
        Args:
            widget: The widget being drawn
            cr: Cairo context for drawing
        
        Returns:
            bool: False to continue propagating the event
        """
        # Get the window dimensions
        width = self.get_allocated_width()
        height = self.get_allocated_height()
        
        # Clear the surface
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        
        # Draw the overlay with the specified color and opacity
        r, g, b = self.color
        cr.set_source_rgba(r, g, b, self.dim_level)
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        
        return False
    
    def set_input_shape(self):
        """Make the window ignore all input events (click-through)."""
        region = cairo.Region()
        self.input_shape_combine_region(region)
    
    def set_dim_level(self, level):
        """
        Set the dimming level.
        
        Args:
            level (float): Dimming level from 0.0 (no dimming) to 1.0 (black)
        """
        # Ensure level is between 0 and 1
        self.dim_level = max(0.0, min(1.0, level))
        
        # Redraw the window
        self.drawing_area.queue_draw()
    
    def set_color(self, color):
        """
        Set the overlay color.
        
        Args:
            color (tuple): RGB color tuple (r, g, b) from 0 to 1
        """
        self.color = color
        
        # Redraw the window
        self.drawing_area.queue_draw()
    
    def on_delete_event(self, widget, event):
        """Handle window close event."""
        return False  # Allow the window to be closed
