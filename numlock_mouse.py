"""This is a module that converts the "5" key to a left mouse click when num-lock is active only."""

import os
import subprocess
from pynput import keyboard
import pyautogui
import threading
import time


def is_numlock_on():
    try:
        output = subprocess.check_output(["xset", "q"]).decode()
        for line in output.split("\n"):
            if "Num Lock:" in line:
                return "on" in line.split("Num Lock:")[1].split()[0]
    except Exception as e:
        print(f"Error checking Num Lock: {e}")
    return False


def handle_numpad5():
    """
    Continuously listen for Numpad 5 key presses.
    If Num Lock is off, simulate a mouse click.
    """

    def on_press(key):
        if hasattr(key, "vk") and key.vk == 101:  # Numpad 5 VK code
            if not is_numlock_on():
                print("Numpad 5 with Num Lock OFF: clicking mouse.")
                pyautogui.click()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()


# Global HotKey callbacks
def on_activate_h():
    print("<ctrl> + <alt> + h pressed")


def on_activate_i():
    print("<ctrl> + <alt> + i pressed")


def on_activate_exit():
    print("<ctrl> + <shift> + q pressed -- exiting...")
    os._exit(0)  # Immediately terminate the program


def main():
    # Thread to monitor Numpad 5 for mouse click behavior
    threading.Thread(target=handle_numpad5, daemon=True).start()

    # Main global hotkey listener
    with keyboard.GlobalHotKeys(
        {
            "<ctrl>+<alt>+q": on_activate_exit,
        }
    ) as hotkeys:
        hotkeys.join()


if __name__ == "__main__":
    main()
