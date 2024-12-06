"""Utility functions for screenshot capture."""

import os
import sys
import time
import platform
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
    try:
        if PLATFORM == "linux":
            import pyscreenshot
            # Try different backends until one works
            backends = ['gnome-screenshot', 'scrot', 'imagemagick', 'qtpy']
            for backend in backends:
                try:
                    pyscreenshot.grab(backend=backend)
                    return "pyscreenshot", backend
                except Exception:
                    continue
            logger.error("No working screenshot backend found")
            sys.exit(1)
        elif PLATFORM == "darwin":
            import pyautogui  # noqa: F401
            return "pyautogui", None
        else:  # windows
            from PIL import ImageGrab  # noqa: F401
            return "pillow", None
    except ImportError as e:
        logger.error("Missing required package: %s", str(e))
        sys.exit(1)


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
logger.info("Using screenshot method: %s with backend: %s", 
            SCREENSHOT_METHOD, SCREENSHOT_COMMAND)


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
            f"round_{device_type}_{round_number}_{event_type}_{timestamp}.png"
        )
        logger.debug("Saving screenshot to: %s", filename)
        
        try:
            if SCREENSHOT_METHOD == "pyscreenshot":
                import pyscreenshot
                screenshot = pyscreenshot.grab(
                    backend=SCREENSHOT_COMMAND,
                    childprocess=True
                )
                screenshot.save(filename)
            elif SCREENSHOT_METHOD == "pyautogui":
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save(filename)
            else:  # pillow
                from PIL import ImageGrab
                screenshot = ImageGrab.grab()
                screenshot.save(filename)
                
        except Exception as e:
            logger.error("Screenshot capture failed: %s", str(e))
            return False
            
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
