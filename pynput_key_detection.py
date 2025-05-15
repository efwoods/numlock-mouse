from pynput import keyboard
import pyautogui
from Xlib.display import Display
import threading
import time


# Hide mouse using X11 (Linux)
def hide_mouse():
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(-10000, 10000)  # move cursor off-screen


# Show mouse at current position
def show_mouse():
    pyautogui.moveTo(pyautogui.position())


class NumLockChecker:
    @staticmethod
    def is_enabled():
        display = Display()
        modmap = display.get_modifier_mapping()
        keycodes = modmap[2]  # Modifier index 2 is Num Lock
        return any(keycode for keycode in keycodes if keycode != 0)


class NumpadListener:
    def __init__(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.num0_held = False
        self.mouse_hidden = True
        self.numlock_state = None
        self.numlock_thread = threading.Thread(
            target=self.poll_numlock_state, daemon=True
        )

    def poll_numlock_state(self):
        # Poll Num Lock state every 0.5 seconds and print if changed
        while True:
            current_state = NumLockChecker.is_enabled()
            if self.numlock_state is None:
                self.numlock_state = current_state
                print(f"Initial Num Lock state: {'ON' if current_state else 'OFF'}")
            elif current_state != self.numlock_state:
                self.numlock_state = current_state
                print(f"Num Lock state changed: {'ON' if current_state else 'OFF'}")
            time.sleep(0.5)

    def on_press(self, key):
        try:
            if key == keyboard.KeyCode.from_vk(96):  # Numpad 0
                if not self.num0_held:
                    self.num0_held = True
                    print("Numpad 0 held. Showing mouse.")
                    if self.mouse_hidden:
                        show_mouse()
                        self.mouse_hidden = False

            elif key == keyboard.KeyCode.from_vk(101):  # Numpad 5
                print("Numpad 5 pressed.")
                if NumLockChecker.is_enabled():
                    print("Num Lock ON. Clicking mouse for Numpad 5.")
                    pyautogui.click()

        except AttributeError:
            pass

        if key == keyboard.Key.esc:
            print("Exiting...")
            self.listener.stop()

    def on_release(self, key):
        if key == keyboard.KeyCode.from_vk(96):  # Numpad 0
            if self.num0_held:
                self.num0_held = False
                print("Numpad 0 released. Hiding mouse.")
                if not self.mouse_hidden:
                    hide_mouse()
                    self.mouse_hidden = True

    def start(self):
        print(
            "Listening for Numpad 5 (click) and Numpad 0 (show/hide mouse). ESC to exit."
        )
        hide_mouse()  # Start with hidden mouse
        self.numlock_thread.start()
        self.listener.start()
        self.listener.join()


if __name__ == "__main__":
    listener = NumpadListener()
    listener.start()
