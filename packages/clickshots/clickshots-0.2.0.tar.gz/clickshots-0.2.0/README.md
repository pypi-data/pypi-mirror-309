# ClickShots

A robust automated screenshot capture system that monitors user interactions and saves screenshots based on configurable triggers.

## Features

- Event-Based Capture: Takes screenshots based on mouse and keyboard events
- Configurable Delays: Prevents spam by enforcing minimum delays between captures
- Toggle Controls: Separate controls for mouse and keyboard monitoring
- Organized Storage: Automatically saves screenshots with descriptive timestamps
- Cross-Platform Support: Works on Linux, macOS, and Windows

## Installation

### From PyPI
```bash
pip install clickshots
```

### For Development
```bash
# Clone the repository
git clone https://github.com/ayon1901/clickshots.git
cd clickshots

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with test dependencies
pip install -e .[test]
```

## Usage

### Command Line
```bash
# Use default directory (~/Pictures/clickshots)
clickshots

# Or specify a custom directory
clickshots -d /path/to/save/directory
```

### Python Code
```python
from clickshots import main

# Use default directory
main()

# Or specify directory
main(save_dir="/path/to/save/directory")
```

## Controls

### Mouse/Touchpad
- **Ctrl + M**: Toggle mouse/touchpad screenshots
- Left click/tap: Capture screenshot (when enabled)

### Keyboard
- **Alt + \\**: Toggle keyboard screenshots
- Space/Enter: Capture screenshot (when enabled)

### General
- **Ctrl + C**: Exit program

## File Naming

Screenshots are saved with descriptive names:
```
round_{device_type}_{round_number}_{event_type}_{timestamp}.png
```

Example: `round_mouse_1_left_click_20240320-143022.png`

## Development

### Running Tests
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=clickshots
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

