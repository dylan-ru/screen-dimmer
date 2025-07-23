#!/usr/bin/env python3
"""
Setup script for Linux Screen Dimmer.

This script installs the Linux Screen Dimmer application.
"""

import os
import sys
from setuptools import setup, find_packages

# Check for required dependencies
try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import Gtk, AppIndicator3
except (ImportError, ValueError) as e:
    print(f"Error: {e}")
    print("Please install the required dependencies:")
    print("  sudo apt-get install python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1")
    sys.exit(1)

# Get the long description from the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="linux-screen-dimmer",
    version="1.0.0",
    description="Reduce screen brightness beyond hardware limits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/linux-screen-dimmer",
    author="Linux Screen Dimmer Team",
    author_email="example@example.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment :: Screen Savers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="screen, brightness, dimmer, overlay",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "PyGObject",
    ],
    entry_points={
        "console_scripts": [
            "linux-screen-dimmer=src.main:main",
        ],
    },
    include_package_data=True,
    data_files=[
        ('share/applications', ['linux-screen-dimmer.desktop']),
        ('share/icons/hicolor/scalable/apps', ['assets/icons/linux-screen-dimmer.svg']),
    ],
    project_urls={
        "Bug Reports": "https://github.com/example/linux-screen-dimmer/issues",
        "Source": "https://github.com/example/linux-screen-dimmer",
    },
)
