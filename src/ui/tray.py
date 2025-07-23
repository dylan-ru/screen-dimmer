#!/usr/bin/env python3
"""
System Tray Icon Implementation

This module provides the system tray icon and menu for the application.
"""

import gi
import os

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Gdk, AppIndicator3, GLib

from src.ui.brightness_dialog import BrightnessDialog
from src.ui.color_picker_dialog import ColorPickerDialog
from src.utils.autostart import toggle_autostart, is_autostart_enabled
from src.config.defaults import APP_NAME, APP_ID

class TrayIcon:
    """
    System tray icon and menu for the application.
    
    This class creates a system tray icon with a menu that includes
    brightness control, color picker, and other options.
    """
    
    def __init__(self, app):
        """
        Initialize the system tray icon.
        
        Args:
            app: The main application instance
        """
        self.app = app
        
        # Create the indicator
        self.indicator = AppIndicator3.Indicator.new(
            APP_ID,
            "display-brightness-symbolic",  # Use a system icon
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        # Create the menu
        self.menu = self.create_menu()
        self.indicator.set_menu(self.menu)
    
    def create_menu(self):
        """
        Create the system tray menu.
        
        Returns:
            Gtk.Menu: The system tray menu
        """
        menu = Gtk.Menu()
        
        # Brightness control
        brightness_item = Gtk.MenuItem(label="Adjust Brightness...")
        brightness_item.connect("activate", self.on_brightness_adjust)
        menu.append(brightness_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Color picker
        color_item = Gtk.MenuItem(label="Change Color...")
        color_item.connect("activate", self.on_color_change)
        menu.append(color_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Autostart option
        self.autostart_item = Gtk.CheckMenuItem(label="Start on Login")
        self.autostart_item.set_active(is_autostart_enabled())
        self.autostart_item.connect("toggled", self.on_autostart_toggled)
        menu.append(self.autostart_item)
        
        # About option
        about_item = Gtk.MenuItem(label="About")
        about_item.connect("activate", self.on_about)
        menu.append(about_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit option
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)
        
        # Show all menu items
        menu.show_all()
        
        return menu
    
    def on_brightness_adjust(self, widget):
        """
        Show the brightness adjustment dialog.
        
        Args:
            widget: The menu item that was activated
        """
        # Create the brightness dialog
        dialog = BrightnessDialog(None, self.app)
        
        # Show the dialog and wait for a response
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            # Get the brightness value from the dialog
            brightness = dialog.get_brightness_value()
            
            # Update the overlay brightness
            self.app.overlay_manager.set_dim_level(brightness)
        
        # Destroy the dialog
        dialog.destroy()
    
    def on_color_change(self, widget):
        """
        Handle color change request.
        
        Args:
            widget: The menu item that was activated
        """
        # Create our custom color picker dialog with dark colors
        dialog = ColorPickerDialog(None, self.app.overlay_manager.color)
        
        # Show the dialog and wait for a response
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            # Get the selected color
            color = dialog.get_selected_color()
            
            # Update the overlay color
            self.app.overlay_manager.set_color(color)
        
        # Destroy the dialog
        dialog.destroy()
    
    def on_autostart_toggled(self, widget):
        """
        Handle autostart option toggle.
        
        Args:
            widget: The check menu item that was toggled
        """
        enabled = widget.get_active()
        toggle_autostart(enabled)
        
        # Update settings
        self.app.settings['autostart'] = enabled
    
    def on_about(self, widget):
        """
        Show the about dialog.
        
        Args:
            widget: The menu item that was activated
        """
        # Create about dialog
        dialog = Gtk.AboutDialog()
        dialog.set_program_name(APP_NAME)
        dialog.set_version("1.0.0")
        dialog.set_copyright("Copyright © 2025")
        dialog.set_comments("Reduce screen brightness beyond hardware limits")
        dialog.set_website("https://github.com/dylan-ru/screen-dimmer")
        dialog.set_logo_icon_name("display-brightness-symbolic")
        
        # Show the dialog
        dialog.run()
        dialog.destroy()
    
    def on_quit(self, widget):
        """
        Quit the application.
        
        Args:
            widget: The menu item that was activated
        """
        self.app.quit()
