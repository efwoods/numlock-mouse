"""This is a module that converts the "5" key to a left mouse click when num-lock is active only."""

import subprocess
import pyautogui
import threading
import time


def is_numlock_on():
    """
    Returns True if Num Lock is active using `xset q`
    """
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
    Waits for the numpad 5 key. If Num Lock is off, click the mouse.
    """
    while True:
        keyboard.wait("kp_5")  # kp_5 is numpad 5
        if not is_numlock_on():
            pyautogui.click()
        # Add a small delay to avoid double-triggers
        time.sleep(0.2)


def main():
    listener = threading.Thread(target=handle_numpad5, daemon=True)
    listener.start()
    print("Listing for Numpad 5... Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
