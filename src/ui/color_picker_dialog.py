#!/usr/bin/env python3
"""
Color Picker Dialog

This module provides a custom color picker dialog with dark colors suitable for screen dimming.
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class ColorPickerDialog(Gtk.Dialog):
    """
    A custom color picker dialog with predefined dark colors.
    
    This dialog provides a selection of dark colors suitable for screen dimming.
    """
    
    # Predefined dark colors (RGB tuples with values from 0 to 1)
    DARK_COLORS = [
        # Pure black
        (0.0, 0.0, 0.0, "Black"),
        
        # Dark grays
        (0.1, 0.1, 0.1, "Dark Gray 1"),
        (0.15, 0.15, 0.15, "Dark Gray 2"),
        (0.2, 0.2, 0.2, "Dark Gray 3"),
        
        # Dark blues
        (0.0, 0.0, 0.1, "Dark Blue 1"),
        (0.0, 0.0, 0.15, "Dark Blue 2"),
        (0.0, 0.0, 0.2, "Dark Blue 3"),
        
        # Dark reds
        (0.1, 0.0, 0.0, "Dark Red 1"),
        (0.15, 0.0, 0.0, "Dark Red 2"),
        (0.2, 0.0, 0.0, "Dark Red 3"),
        
        # Dark greens
        (0.0, 0.1, 0.0, "Dark Green 1"),
        (0.0, 0.15, 0.0, "Dark Green 2"),
        (0.0, 0.2, 0.0, "Dark Green 3"),
        
        # Dark amber (for night mode)
        (0.2, 0.1, 0.0, "Dark Amber 1"),
        (0.15, 0.075, 0.0, "Dark Amber 2"),
        (0.1, 0.05, 0.0, "Dark Amber 3"),
    ]
    
    def __init__(self, parent, current_color):
        """
        Initialize the color picker dialog.
        
        Args:
            parent: The parent window
            current_color: The current color as an RGB tuple (r, g, b)
        """
        super().__init__(
            title="Select Overlay Color",
            transient_for=parent,
            flags=Gtk.DialogFlags.MODAL
        )
        
        # Set dialog position to appear near the mouse cursor
        self.set_position(Gtk.WindowPosition.MOUSE)
        
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
        label = Gtk.Label(label="Select a dark color for the overlay:")
        content_area.add(label)
        
        # Create a grid for color buttons
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        content_area.add(grid)
        
        # Create color buttons
        self.color_buttons = []
        row = 0
        col = 0
        max_cols = 4
        
        for i, (r, g, b, name) in enumerate(self.DARK_COLORS):
            # Create a button with the color
            button = Gtk.Button()
            button.set_size_request(50, 30)
            
            # Create a color swatch
            color_box = Gtk.EventBox()
            color_box.set_size_request(50, 30)
            
            # Set the background color
            rgba = Gdk.RGBA()
            rgba.red = r
            rgba.green = g
            rgba.blue = b
            rgba.alpha = 1.0
            color_box.override_background_color(Gtk.StateFlags.NORMAL, rgba)
            
            # Add the color swatch to the button
            button.add(color_box)
            
            # Store the color with the button
            button.color = (r, g, b)
            button.connect("clicked", self.on_color_selected)
            
            # Add a tooltip with the color name
            button.set_tooltip_text(name)
            
            # Add the button to the grid
            grid.attach(button, col, row, 1, 1)
            self.color_buttons.append(button)
            
            # Update row and column
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Store the selected color
        self.selected_color = current_color
        
        # Show all widgets
        self.show_all()
    
    def on_color_selected(self, button):
        """
        Handle color button click.
        
        Args:
            button: The button that was clicked
        """
        # Update the selected color
        self.selected_color = button.color
        
        # Highlight the selected button
        for btn in self.color_buttons:
            if btn == button:
                btn.set_relief(Gtk.ReliefStyle.NORMAL)
            else:
                btn.set_relief(Gtk.ReliefStyle.NONE)
    
    def get_selected_color(self):
        """
        Get the selected color.
        
        Returns:
            tuple: The selected color as an RGB tuple (r, g, b)
        """
        return self.selected_color
