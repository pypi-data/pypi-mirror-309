"""Tests for the clickshots package."""

import os
import pytest
from unittest.mock import patch, MagicMock
from pynput import keyboard, mouse
from clickshots.listeners import ScreenshotListener
from clickshots.utils import (
    setup_screenshot_method, 
    validate_directory,
    get_last_round_number
)


@pytest.fixture
def mock_environment():
    """Set up test environment."""
    with patch('platform.system', return_value='Linux'), \
         patch('pyscreenshot.grab') as mock_grab, \
         patch.dict('sys.modules', {
             'pyautogui': MagicMock(),
             'PIL': MagicMock(),
             'PIL.ImageGrab': MagicMock()
         }):
        mock_image = MagicMock()
        mock_image.save = MagicMock(
            side_effect=lambda x: open(x, 'w').close()
        )
        mock_grab.return_value = mock_image
        yield


@pytest.fixture
def test_listener(tmp_path):
    """Create a test listener with a temporary directory."""
    test_dir = str(tmp_path / "screenshots")
    os.makedirs(test_dir, exist_ok=True)
    return ScreenshotListener(save_dir=test_dir)


def test_screenshot_listener_init(test_listener):
    """Test ScreenshotListener initialization."""
    assert test_listener.mouse_screenshot_enabled is False
    assert test_listener.keyboard_screenshot_enabled is False
    assert test_listener.mouse_round_counter == 0
    assert test_listener.keyboard_round_counter == 0
    assert isinstance(test_listener.button_states, dict)
    assert isinstance(test_listener.key_states, dict)


def test_should_capture(test_listener):
    """Test screenshot capture timing logic."""
    # Test mouse events when disabled
    assert not test_listener.should_capture("left_click")
    
    # Test keyboard events when disabled
    assert not test_listener.should_capture("word_complete")
    
    # Enable mouse screenshots and test
    test_listener.mouse_screenshot_enabled = True
    assert test_listener.should_capture("left_click")
    
    # Test delay between captures
    assert not test_listener.should_capture("left_click")


def test_mouse_toggle(test_listener):
    """Test mouse screenshot toggle functionality."""
    # Simulate Ctrl + M press
    test_listener.key_states[keyboard.Key.ctrl_l] = True
    key = MagicMock()
    key.char = 'm'
    
    test_listener.on_press(key)
    assert test_listener.mouse_screenshot_enabled is True
    
    test_listener.on_press(key)
    assert test_listener.mouse_screenshot_enabled is False


def test_keyboard_toggle(test_listener):
    """Test keyboard screenshot toggle functionality."""
    # Simulate Alt + \ press
    test_listener.key_states[keyboard.Key.alt_l] = True
    key = MagicMock()
    key.char = '\\'
    
    test_listener.on_press(key)
    assert test_listener.keyboard_screenshot_enabled is True
    
    test_listener.on_press(key)
    assert test_listener.keyboard_screenshot_enabled is False


def test_mouse_click_capture(test_listener, mock_environment):
    """Test mouse click screenshot capture."""
    test_listener.mouse_screenshot_enabled = True
    
    # Simulate left click
    test_listener.on_click(
        x=100, 
        y=100, 
        button=mouse.Button.left, 
        pressed=True
    )
    
    assert test_listener.button_states[mouse.Button.left] is True


def test_keyboard_capture(test_listener, mock_environment):
    """Test keyboard screenshot capture."""
    test_listener.keyboard_screenshot_enabled = True
    
    # Simulate space key press
    test_listener.on_press(keyboard.Key.space)
    
    # Simulate enter key press
    test_listener.on_press(keyboard.Key.enter)


def test_round_number_tracking(tmp_path):
    """Test round number tracking functionality."""
    test_dir = str(tmp_path / "screenshots")
    os.makedirs(test_dir, exist_ok=True)
    
    # Create some test files
    test_files = [
        f"round_mouse_1_left_click_20240320-143022.png",
        f"round_keyboard_2_word_complete_20240320-143023.png",
        f"round_mouse_3_left_click_20240320-143024.png"
    ]
    
    for file in test_files:
        with open(os.path.join(test_dir, file), 'w') as f:
            f.write("test")
    
    assert get_last_round_number(test_dir) == 3


def test_screenshot_method_setup(mock_environment):
    """Test platform-specific screenshot method setup."""
    method, command = setup_screenshot_method()
    assert method == "pyscreenshot"
    assert command in ['gnome-screenshot', 'scrot', 'imagemagick', 'qtpy']


def test_validate_directory(tmp_path):
    """Test directory validation."""
    test_dir = tmp_path / "test_screenshots"
    assert validate_directory(str(test_dir)) is True
    assert os.path.exists(test_dir)


def test_capture_screenshot(mock_environment, tmp_path):
    """Test screenshot capture functionality."""
    from clickshots.utils import capture_screenshot
    
    test_dir = str(tmp_path / "screenshots")
    os.makedirs(test_dir, exist_ok=True)
    
    result = capture_screenshot(
        event_type="left_click",
        round_number=1,
        device_type="mouse",
        save_dir=test_dir
    )
    
    assert result is True
    assert os.path.exists(test_dir)
    # Check if a file was created
    files = os.listdir(test_dir)
    assert len(files) == 1
    assert files[0].startswith("round_mouse_1_left_click")


@pytest.mark.parametrize("platform", ["linux", "darwin", "windows"])
def test_platform_specific_setup(platform):
    """Test screenshot method setup for different platforms."""
    with patch('platform.system', return_value=platform.capitalize()), \
         patch('clickshots.utils.PLATFORM', platform), \
         patch.dict('sys.modules', {
             'pyscreenshot': MagicMock(),
             'pyautogui': MagicMock(),
             'PIL': MagicMock(),
             'PIL.ImageGrab': MagicMock()
         }):
        
        if platform == "linux":
            with patch('pyscreenshot.grab') as mock_grab:
                mock_grab.return_value = MagicMock()
                method, command = setup_screenshot_method()
                assert method == "pyscreenshot"
                assert command in ['gnome-screenshot', 'scrot', 'imagemagick', 'qtpy']
        
        elif platform == "darwin":
            with patch('pyautogui.screenshot') as mock_screenshot:
                mock_screenshot.return_value = MagicMock()
                method, command = setup_screenshot_method()
                assert method == "pyautogui"
                assert command is None
        
        else:  # windows
            with patch('PIL.ImageGrab.grab') as mock_grab:
                mock_grab.return_value = MagicMock()
                method, command = setup_screenshot_method()
                assert method == "pillow"
                assert command is None


def test_error_handling(test_listener):
    """Test error handling in listeners."""
    # Test invalid key press
    test_listener.on_press(None)
    
    # Test invalid mouse click
    test_listener.on_click(0, 0, None, True)
    
    # Test stopping non-started listeners
    test_listener.stop()