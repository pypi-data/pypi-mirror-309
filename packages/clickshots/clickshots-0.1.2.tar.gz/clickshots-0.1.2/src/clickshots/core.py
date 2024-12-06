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


def main(save_dir=None):
    """
    Main entry point for the application.
    
    Args:
        save_dir (str, optional): Directory to save screenshots.
            Defaults to ~/Pictures/clickshot
    """
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
    
    listener = ScreenshotListener(save_dir=save_dir)
    try:
        listener.start()
    except KeyboardInterrupt:
        print("\nStopping listeners...")
        listener.stop()
        sys.exit(0)


if __name__ == "__main__":
    main()
