#!/usr/bin/env python3
"""
Display Utilities

This module provides utilities for detecting and managing displays.
"""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkX11

def get_monitors():
    """
    Get all connected monitors.
    
    Returns:
        list: List of Gdk.Monitor objects
    """
    display = Gdk.Display.get_default()
    monitors = []
    
    # Get all monitors
    n_monitors = display.get_n_monitors()
    for i in range(n_monitors):
        monitors.append(display.get_monitor(i))
    
    return monitors

def get_monitor_info():
    """
    Get information about all connected monitors.
    
    Returns:
        list: List of dictionaries with monitor information
    """
    monitors = get_monitors()
    monitor_info = []
    
    for monitor in monitors:
        geometry = monitor.get_geometry()
        info = {
            'id': str(monitor.get_model()),
            'name': monitor.get_model(),
            'manufacturer': monitor.get_manufacturer(),
            'width': geometry.width,
            'height': geometry.height,
            'x': geometry.x,
            'y': geometry.y,
            'scale_factor': monitor.get_scale_factor(),
            'primary': monitor.is_primary()
        }
        monitor_info.append(info)
    
    return monitor_info

def get_primary_monitor():
    """
    Get the primary monitor.
    
    Returns:
        Gdk.Monitor: The primary monitor
    """
    display = Gdk.Display.get_default()
    return display.get_primary_monitor()

def get_monitor_at_position(x, y):
    """
    Get the monitor at the specified position.
    
    Args:
        x (int): X coordinate
        y (int): Y coordinate
    
    Returns:
        Gdk.Monitor: The monitor at the specified position
    """
    display = Gdk.Display.get_default()
    return display.get_monitor_at_point(x, y)

def get_monitor_for_window(window):
    """
    Get the monitor that contains the specified window.
    
    Args:
        window (Gtk.Window): The window to check
    
    Returns:
        Gdk.Monitor: The monitor containing the window
    """
    display = Gdk.Display.get_default()
    gdk_window = window.get_window()
    if gdk_window:
        return display.get_monitor_at_window(gdk_window)
    return display.get_primary_monitor()
