"""Core functionality for screenshot capture."""

import sys
import argparse
from .listeners import ScreenshotListener
from .utils import validate_directory, DEFAULT_SCREENSHOT_DIR


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Automated screenshot capture system"
    )
    parser.add_argument(
        "-d", "--directory",
        help="Directory to save screenshots (default: ~/Pictures/clickshot)",
        default=DEFAULT_SCREENSHOT_DIR
    )
    return parser.parse_args()


def print_instructions():
    """Print usage instructions."""
    print("\nTouchpad Controls:")
    print("- Single tap: Left click")
    print("- Two-finger tap: Right click")
    print("- Three-finger tap + Left click: Toggle screenshot capture")
    print("- Two-finger scroll: Scroll capture")
    print("- Pinch gesture: Pinch capture")
    print("\nKeyboard Controls:")
    print("- Ctrl + M: Toggle mouse/touchpad screenshots")
    print("- Alt + \\: Toggle keyboard screenshots")
    print("- Space/Enter: Capture screenshot (when keyboard mode enabled)")
    print("- Ctrl + C: Exit program")


def main(save_dir=None):
    """Main entry point for the application."""
    try:
        # If no directory provided, check command line args
        if save_dir is None:
            args = parse_args()
            save_dir = args.directory
        
        # Validate directory
        if not validate_directory(save_dir):
            print("Using default directory:", DEFAULT_SCREENSHOT_DIR)
            save_dir = DEFAULT_SCREENSHOT_DIR
            if not validate_directory(save_dir):
                print("Cannot write to any directory. Exiting.")
                sys.exit(1)

        print("Screenshot capture started. Press Ctrl+C to exit.")
        print("\nConfiguration:")
        print("- Screenshots taken every 2 seconds for clicks/scrolls")
        print("- Screenshots will be taken for space and enter keys")
        print_instructions()
        
        listener = ScreenshotListener(save_dir=save_dir)
        listener.start()
        
    except KeyboardInterrupt:
        print("\nStopping listeners...")
        if 'listener' in locals():
            listener.stop()
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
