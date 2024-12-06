"""Event listeners for screenshot capture."""

from datetime import datetime, timedelta
import time
from pynput import mouse, keyboard
from .utils import DELAY_CONFIG, capture_screenshot, get_last_round_number


class ScreenshotListener:
    """Manages mouse and keyboard listeners for screenshot capture."""
    
    def __init__(self, save_dir=None):
        self.mouse_listener = None
        self.keyboard_listener = None
        self._running = False
        self.mouse_screenshot_enabled = False
        self.keyboard_screenshot_enabled = False
        self.mouse_round_counter = 0
        self.keyboard_round_counter = 0
        self.last_screenshot_time = {}
        self.button_states = {
            mouse.Button.left: False,
        }
        self.key_states = {
            keyboard.Key.alt_l: False,
            keyboard.Key.alt_r: False,
            keyboard.Key.ctrl_l: False,
            keyboard.Key.ctrl_r: False,
        }
        self.save_dir = save_dir

    def should_capture(self, event_type):
        """Check if screenshot capture is allowed based on timing and state."""
        if event_type in ["left_click", "right_click", "middle_click"]:
            if not self.mouse_screenshot_enabled:
                return False
                
        if event_type == "word_complete":
            if not self.keyboard_screenshot_enabled:
                return False
        
        current_time = datetime.now()
        if event_type not in self.last_screenshot_time:
            delay = timedelta(seconds=DELAY_CONFIG[event_type])
            self.last_screenshot_time[event_type] = current_time - delay
        
        time_delta = current_time - self.last_screenshot_time[event_type]
        time_passed = time_delta.total_seconds()
        
        if time_passed >= DELAY_CONFIG[event_type]:
            self.last_screenshot_time[event_type] = current_time
            return True
        return False

    def on_click(self, x, y, button, pressed):
        """Handle mouse click events."""
        if button == mouse.Button.left:
            self.button_states[button] = pressed
            
            if pressed and self.mouse_screenshot_enabled:
                try:
                    capture_screenshot(
                        event_type="left_click",
                        round_number=self.mouse_round_counter,
                        device_type="mouse",
                        save_dir=self.save_dir
                    )
                except Exception as e:
                    print(f"Input detection error: {e}")

    def on_press(self, key):
        """Handle keyboard press events."""
        try:
            # Update key states
            if key in self.key_states:
                self.key_states[key] = True
            
            # Check for Ctrl + M combination for mouse/touchpad toggle
            ctrl_pressed = (self.key_states[keyboard.Key.ctrl_l] or 
                          self.key_states[keyboard.Key.ctrl_r])
            if (ctrl_pressed and hasattr(key, 'char') and key.char == 'm'):
                self.mouse_screenshot_enabled = not self.mouse_screenshot_enabled
                if self.mouse_screenshot_enabled:
                    self.mouse_round_counter = (
                        get_last_round_number(self.save_dir) + 1
                    )
                status = "enabled" if self.mouse_screenshot_enabled else "disabled"
                print(f"\nMouse/touchpad screenshot capturing {status}")
                if self.mouse_screenshot_enabled:
                    print(f"Starting round {self.mouse_round_counter}")
                return
            
            # Check for Alt + \ combination
            alt_pressed = (self.key_states[keyboard.Key.alt_l] or 
                            self.key_states[keyboard.Key.alt_r])
            if hasattr(key, 'char') and key.char == '\\' and alt_pressed:
                self.keyboard_screenshot_enabled = not self.keyboard_screenshot_enabled
                if self.keyboard_screenshot_enabled:
                    self.keyboard_round_counter = (
                        get_last_round_number(self.save_dir) + 1
                    )
                status = ("enabled" if self.keyboard_screenshot_enabled 
                         else "disabled")
                print(f"\nKeyboard screenshot capturing {status}")
                if self.keyboard_screenshot_enabled:
                    print(f"Starting round {self.keyboard_round_counter}")
                return
            
            # Handle space/enter key screenshots
            if self.keyboard_screenshot_enabled:
                if key in [keyboard.Key.space, keyboard.Key.enter]:
                    capture_screenshot(
                        event_type="word_complete",
                        round_number=self.keyboard_round_counter,
                        device_type="keyboard",
                        save_dir=self.save_dir
                    )
                    
        except Exception as e:
            print(f"Keyboard detection error: {e}")

    def on_release(self, key):
        """Handle keyboard release events."""
        if key in self.key_states:
            self.key_states[key] = False

    def start(self):
        """Start the mouse and keyboard listeners."""
        try:
            self._running = True
            
            self.mouse_listener = mouse.Listener(on_click=self.on_click)
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )

            self.mouse_listener.start()
            self.keyboard_listener.start()

            next_round = get_last_round_number(self.save_dir) + 1
            print(f"\nContinuing from round {next_round}")

            while self._running:
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nReceived interrupt signal...")
            self.stop()
        except Exception as e:
            print(f"Error in listeners: {e}")
        finally:
            self.stop()

    def stop(self):
        """Stop all listeners and clean up."""
        self._running = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        print("Listeners stopped.")
