from pynput import keyboard
import pyautogui
from Xlib.display import Display
import ctypes
import threading


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
        return any(kc for kc in keycodes if kc != 0)


class NumpadListener:
    def __init__(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.num0_held = False
        self.mouse_hidden = True

    def on_press(self, key):
        try:
            if key == keyboard.KeyCode.from_vk(96):  # Numpad 0
                if not self.num0_held:
                    self.num0_held = True
                    if self.mouse_hidden:
                        print("Numpad 0 held. showing mouse.")
                        show_mouse()
                        self.mouse_hidden = False
            elif key == keyboard.KeyCode.from_vk(101):  # Numpad 5
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
            if self.num0_held == False:
                if not self.mouse_hidden:
                    print("Numpad 0 released. Hiding mouse.")
                    hide_mouse()
                    self.mouse_hidden = True

    def start(self):
        print(
            "Listening for Numpad 5 (click) and Numpad 0 (show/hide mouse). ESC to exit."
        )
        hide_mouse()  # Start with hidden mouse
        self.listener.start()
        self.listener.join()


class KeyComboListener:
    def __init__(self, combination):
        self.combination = combination
        self.pressed_keys = set()
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )

    def on_press(self, key):
        self.pressed_keys.add(key)

        if self.combination.issubset(self.pressed_keys):
            print("Detected Ctrl + Alt + K!")

    def on_release(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

        if key == keyboard.Key.esc:
            print("Exiting...")
            self.listener.stop()  # Stop the listener cleanly

    def start(self):
        print("Listening for Ctrl + Alt + K. Press ESC to exit.")
        self.listener.start()
        self.listener.join()


def drive_numpad_listener():
    listener = NumpadListener()
    listener.start()


def drive_keyboard_keycombo_listener():
    combo = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char="k")}
    listener = KeyComboListener(combo)
    listener.start()


if __name__ == "__main__":
    drive_numpad_listener()
