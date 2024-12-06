"""Tests for the clickshots package."""

from clickshots.listeners import ScreenshotListener
from clickshots.utils import setup_screenshot_method


def test_screenshot_listener_init():
    """Test ScreenshotListener initialization."""
    listener = ScreenshotListener()
    assert listener.mouse_screenshot_enabled is False
    assert listener.keyboard_screenshot_enabled is False
    assert listener.mouse_round_counter == 0
    assert listener.keyboard_round_counter == 0


def test_should_capture():
    """Test screenshot capture timing logic."""
    listener = ScreenshotListener()
    
    # Test mouse events when disabled
    assert not listener.should_capture("tap")
    assert not listener.should_capture("right_tap")
    
    # Test keyboard events when disabled
    assert not listener.should_capture("word_complete")
    
    # Enable mouse screenshots
    listener.mouse_screenshot_enabled = True
    assert listener.should_capture("tap")
    
    # Test delay between captures
    assert not listener.should_capture("tap")  # Should be blocked by delay


def test_screenshot_method_setup():
    """Test platform-specific screenshot method setup."""
    method, command = setup_screenshot_method()
    assert method in ["command_line", "pyautogui", "pillow"]
