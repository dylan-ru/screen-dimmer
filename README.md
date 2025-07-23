# Screen Dimmer

A lightweight application that reduces screen brightness beyond hardware limits by creating a transparent overlay.

## Features

- Reduce screen brightness beyond hardware limits
- System tray integration with brightness slider
- Support for multiple monitors
- Customizable overlay color
- Persistent settings between sessions
- Autostart capability
- Low resource usage

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/dylan-ru/screen-dimmer.git
   cd screen-dimmer
   ```

2. Install dependencies:
   ```bash
   sudo apt-get install python3 python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 python3-cairo gir1.2-gdkpixbuf-2.0
   ```

3. Install the application:
   ```bash
   python3 setup.py install --user
   ```

### From Package (Debian/Ubuntu)

1. Download the latest .deb package from the [releases page](https://github.com/dylan-ru/screen-dimmer/releases).

2. Install the package:
   ```bash
   sudo dpkg -i screen-dimmer_1.0.0_all.deb
   sudo apt-get install -f  # Install dependencies if needed
   ```

## Usage

1. Launch the application from your applications menu or run:
   ```bash
   screen-dimmer
   ```

2. Adjust the brightness using the slider in the system tray menu.

3. Customize the overlay color by selecting "Change Color" from the menu.

4. Enable "Start on Login" to automatically start the application when you log in.

## Dependencies

The application requires the following dependencies:

- Python 3 (>= 3.6)
- PyGObject (python3-gi)
- GTK 3 bindings (gir1.2-gtk-3.0)
- AppIndicator3 bindings (gir1.2-appindicator3-0.1)
- Cairo bindings (python3-cairo)
- GDK Pixbuf bindings (gir1.2-gdkpixbuf-2.0)

These dependencies will be automatically installed when using the Debian package. If installing from source, you'll need to install them manually.

## Building a Debian Package

To build a Debian package:

1. Install the required tools:
   ```bash
   sudo apt-get install devscripts debhelper dh-python
   ```

2. Build the package:
   ```bash
   cd screen-dimmer
   debuild -us -uc
   ```

3. The .deb package will be created in the parent directory.

Alternatively, you can use the provided packaging script:

```bash
./scripts/build_deb.sh
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by [Desktop Dimmer](https://github.com/sidneys/desktop-dimmer) and [PangoBright](https://pangobright.com/)
