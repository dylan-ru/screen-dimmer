#!/usr/bin/env python3
"""
Brightness Dialog

This module provides a dialog for adjusting screen brightness.
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

from src.config.defaults import MAX_DIM_LEVEL

class BrightnessDialog(Gtk.Dialog):
    """
    A dialog for adjusting screen brightness.
    
    This dialog contains a slider that allows users to adjust
    the dimming level of the screen overlay.
    """
    
    def __init__(self, parent, app):
        """
        Initialize the brightness dialog.
        
        Args:
            parent: The parent window
            app: The main application instance
        """
        super().__init__(
            title="Adjust Brightness",
            transient_for=parent,
            flags=Gtk.DialogFlags.MODAL
        )
        
        self.app = app
        
        # Set dialog position to appear near the mouse cursor
        self.set_position(Gtk.WindowPosition.MOUSE)
        
        # Set window gravity to ensure it appears above the cursor
        self.set_gravity(Gdk.Gravity.SOUTH)
        
        # Set a reasonable size for the dialog
        self.set_default_size(350, -1)
        
        # Add buttons
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        
        # Create content area
        content_area = self.get_content_area()
        content_area.set_spacing(10)
        content_area.set_margin_top(10)
        content_area.set_margin_bottom(10)
        content_area.set_margin_start(10)
        content_area.set_margin_end(10)
        
        # Create a label
        label = Gtk.Label(label="Adjust screen brightness:")
        content_area.add(label)
        
        # Create a box for the slider and value display with minimal spacing
        slider_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        content_area.add(slider_box)
        
        # Create adjustment (0 to MAX_DIM_LEVEL)
        adjustment = Gtk.Adjustment(
            value=app.overlay_manager.dim_level,
            lower=0.0,
            upper=MAX_DIM_LEVEL,
            step_increment=0.01,
            page_increment=0.1,
            page_size=0
        )
        
        # Create the slider
        self.slider = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL,
            adjustment=adjustment
        )
        
        # Configure the slider
        self.slider.set_size_request(270, -1)  # Adjusted width
        self.slider.set_draw_value(False)  # Don't draw the value on the slider
        self.slider.set_has_origin(True)
        self.slider.set_show_fill_level(True)
        self.slider.set_fill_level(MAX_DIM_LEVEL)
        self.slider.set_restrict_to_fill_level(True)
        
        # Add marks
        self.slider.add_mark(0.0, Gtk.PositionType.BOTTOM, "0%")
        self.slider.add_mark(MAX_DIM_LEVEL / 2, Gtk.PositionType.BOTTOM, "50%")
        self.slider.add_mark(MAX_DIM_LEVEL, Gtk.PositionType.BOTTOM, "100%")
        
        # Create a separate label for the value display
        self.value_label = Gtk.Label(label=f"{adjustment.get_value():.2f}")
        self.value_label.set_size_request(40, -1)  # Compact width for the value label
        self.value_label.set_xalign(0.0)  # Left-align the text
        self.value_label.set_valign(Gtk.Align.CENTER)  # Center vertically
        
        # Create an event box to handle the value label's background
        value_event_box = Gtk.EventBox()
        value_event_box.add(self.value_label)
        
        # Add the slider and value label to the box with proper packing
        slider_box.pack_start(self.slider, True, True, 0)
        slider_box.pack_start(value_event_box, False, False, 0)
        
        # Connect to value-changed signal for live preview and value update
        self.slider.connect("value-changed", self.on_value_changed)
        
        # Add a timeout to avoid too frequent updates
        self.timeout_id = None
        
        # Show all widgets
        self.show_all()
        
        # Position the dialog near the system tray area (bottom-right)
        self.position_near_systray()
    
    def position_near_systray(self):
        """Position the dialog near the system tray area."""
        # Get the screen dimensions
        screen = Gdk.Screen.get_default()
        monitor = screen.get_primary_monitor()
        geometry = screen.get_monitor_geometry(monitor)
        
        # Get the dialog dimensions
        dialog_width, dialog_height = self.get_size()
        
        # Position the dialog in the bottom-right corner, but above the panel
        x = geometry.width - dialog_width - 20  # 20 pixels from the right edge
        y = geometry.height - dialog_height - 60  # Above the panel (assuming 30px panel height)
        
        # Move the dialog to the calculated position
        self.move(x, y)
    
    def on_value_changed(self, widget):
        """
        Handle slider value changes.
        
        Args:
            widget: The slider widget
        """
        # Get the current value
        value = widget.get_value()
        
        # Update the value label
        self.value_label.set_text(f"{value:.2f}")
        
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
    
    def get_brightness_value(self):
        """
        Get the current brightness value.
        
        Returns:
            float: The current brightness value
        """
        return self.slider.get_value()
