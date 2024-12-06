"""Event listeners for screenshot capture."""

from datetime import datetime, timedelta
import time
from pynput import mouse, keyboard
from .utils import DELAY_CONFIG, capture_screenshot


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
            mouse.Button.right: False,
            'tap_time': 0,
            'last_x': 0,
            'last_y': 0,
        }
        self.key_states = {
            keyboard.Key.alt_l: False,
            keyboard.Key.alt_r: False,
        }
        self.current_keys = set()
        self.MOUSE_TOGGLE_KEYS = {keyboard.Key.ctrl_l, keyboard.Key.shift_l}
        self.save_dir = save_dir

    def should_capture(self, event_type):
        """Check if screenshot capture is allowed based on timing and state."""
        if event_type in ["tap", "right_tap"]:
            if not self.mouse_screenshot_enabled:
                return False
                
        if event_type == "word_complete":
            if not self.keyboard_screenshot_enabled:
                return False
        
        current_time = datetime.now()
        if event_type not in self.last_screenshot_time:
            delay = timedelta(seconds=DELAY_CONFIG[event_type])
            self.last_screenshot_time[event_type] = current_time - delay
        
        last_time = self.last_screenshot_time[event_type]
        time_passed = (current_time - last_time).total_seconds()
        
        if time_passed >= DELAY_CONFIG[event_type]:
            self.last_screenshot_time[event_type] = current_time
            return True
        return False

    def on_click(self, x, y, button, pressed):
        """Handle mouse click events."""
        if button in self.button_states:
            self.button_states[button] = pressed

        if pressed and self.mouse_screenshot_enabled:
            if button == mouse.Button.left:
                capture_screenshot(
                    event_type="tap",
                    round_number=self.mouse_round_counter,
                    device_type="mouse",
                    save_dir=self.save_dir
                )
            elif button == mouse.Button.right:
                capture_screenshot(
                    event_type="right_tap",
                    round_number=self.mouse_round_counter,
                    device_type="mouse",
                    save_dir=self.save_dir
                )

    def on_press(self, key):
        """Handle keyboard press events."""
        try:
            if key in self.key_states:
                self.key_states[key] = True
                
            self.current_keys.add(key)
            
            # Toggle mouse capture with Ctrl+Shift
            if self.MOUSE_TOGGLE_KEYS.issubset(self.current_keys):
                self.mouse_screenshot_enabled = not self.mouse_screenshot_enabled
                if self.mouse_screenshot_enabled:
                    self.mouse_round_counter += 1
                status = "enabled" if self.mouse_screenshot_enabled else "disabled"
                print("\nMouse screenshot capturing", status)
                return
                
            # Toggle keyboard capture with Alt+\
            alt_pressed = (self.key_states[keyboard.Key.alt_l] or 
                         self.key_states[keyboard.Key.alt_r])
            if hasattr(key, 'char') and key.char == '\\' and alt_pressed:
                self.keyboard_screenshot_enabled = not self.keyboard_screenshot_enabled
                if self.keyboard_screenshot_enabled:
                    self.keyboard_round_counter += 1
                status = "enabled" if self.keyboard_screenshot_enabled else "disabled"
                print("\nKeyboard screenshot capturing", status)
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
            print("Keyboard detection error:", e)

    def on_release(self, key):
        """Handle keyboard release events."""
        if key in self.key_states:
            self.key_states[key] = False
        self.current_keys.discard(key)

    def start(self):
        """Start the mouse and keyboard listeners."""
        try:
            self._running = True
            
            self.mouse_listener = mouse.Listener(
                on_click=self.on_click
            )
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )

            self.mouse_listener.start()
            self.keyboard_listener.start()

            print("\nScreenshot capture started. Use the following controls:")
            print("- Ctrl + Shift: Toggle mouse/touchpad screenshots")
            print("- Alt + \\: Toggle keyboard screenshots")
            print("- Ctrl + C: Exit program")

            while self._running:
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nReceived interrupt signal...")
            self.stop()
        except Exception as e:
            print("Error in listeners:", e)
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
