"""Utility functions for screenshot capture."""

import os
import sys
import time
import platform
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Platform detection
PLATFORM = platform.system().lower()

# Configuration constants
DELAY_CONFIG = {
    "tap": 2,
    "right_tap": 2,
    "word_complete": 2,
}

# Default screenshot directory
DEFAULT_SCREENSHOT_DIR = os.path.join(
    os.path.expanduser("~"),
    "Pictures" if PLATFORM != "windows" else "My Pictures", 
    "clickshots"
)


def setup_screenshot_method():
    """Configure screenshot method based on platform."""
    if PLATFORM == "linux":
        if check_command_exists('gnome-screenshot'):
            return "command_line", 'gnome-screenshot'
        else:
            logger.error("Please install gnome-screenshot")
            sys.exit(1)
    elif PLATFORM == "darwin":
        try:
            import pyautogui
            return "pyautogui", None
        except ImportError:
            logger.error("Please install pyautogui: pip install pyautogui")
            sys.exit(1)
    elif PLATFORM == "windows":
        try:
            from PIL import ImageGrab
            return "pillow", None
        except ImportError:
            logger.error("Please install Pillow: pip install Pillow")
            sys.exit(1)
    else:
        logger.error("Unsupported platform: " + PLATFORM)
        sys.exit(1)


def check_command_exists(command):
    """Check if a command exists on Linux."""
    try:
        result = subprocess.run(
            ['which', command],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def validate_directory(directory):
    """Validate and create directory if it doesn't exist."""
    try:
        logger.debug("Creating directory: %s", directory)
        os.makedirs(directory, exist_ok=True)
        
        # Test write permissions
        test_file = os.path.join(directory, "test.txt")
        logger.debug("Testing write permissions with: %s", test_file)
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        logger.debug("Directory %s is writable", directory)
        return True
    except Exception as e:
        logger.error("Error with directory %s: %s", directory, str(e))
        return False


SCREENSHOT_METHOD, SCREENSHOT_COMMAND = setup_screenshot_method()
logger.info("Using screenshot method: %s", SCREENSHOT_METHOD)


def capture_screenshot(event_type="event", round_number=0, device_type="mouse",
                      save_dir=None):
    """Cross-platform screenshot capture function."""
    try:
        screenshot_dir = save_dir if save_dir else DEFAULT_SCREENSHOT_DIR
        logger.debug("Using screenshot directory: %s", screenshot_dir)
        
        if not validate_directory(screenshot_dir):
            logger.warning("Cannot use %s, trying default", screenshot_dir)
            screenshot_dir = DEFAULT_SCREENSHOT_DIR
            if not validate_directory(screenshot_dir):
                logger.error("Cannot write to any directory")
                sys.exit(1)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(
            screenshot_dir,
            f"round_{device_type}_{round_number}_screenshot_{event_type}"
            f"_{timestamp}.png"
        )
        logger.debug("Saving screenshot to: %s", filename)
        
        if SCREENSHOT_METHOD == "command_line":
            env = os.environ.copy()
            env["DISPLAY"] = ":0"
            env["GNOME_SCREENSHOT_SILENCE"] = "1"  # Try to silence notifications
            env["NO_AT_BRIDGE"] = "1"  # Disable accessibility
            
            if SCREENSHOT_COMMAND == 'gnome-screenshot':
                # Use gnome-screenshot with minimal feedback
                result = subprocess.run(
                    [
                        'gnome-screenshot',
                        '--file', filename,  # Save to file
                        '--border-effect', 'none',  # No effects
                        '--include-border',  # Include window borders
                        '--display', ':0'    # Specify display
                    ],
                    capture_output=True,
                    text=True,
                    env=env
                )
                
                if result.returncode != 0:
                    logger.error("Screenshot failed: %s", result.stderr)
                    return False
                    
        elif SCREENSHOT_METHOD == "pyautogui":
            import pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
        elif SCREENSHOT_METHOD == "pillow":
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            screenshot.save(filename)
            
        if os.path.exists(filename):
            logger.info("Screenshot saved: %s", filename)
            print("Screenshot saved in:", screenshot_dir)
            print("Filename:", os.path.basename(filename))
            return True
        else:
            logger.error("Screenshot file not created: %s", filename)
            return False
        
    except Exception as e:
        logger.error("Screenshot failed: %s", str(e))
        import traceback
        logger.error(traceback.format_exc())
        return False
