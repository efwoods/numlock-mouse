from pynput import keyboard
import subprocess
import pyautogui


def is_numlock_on():
    result = subprocess.run(["xset", "q"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "LED mask" in line:
            led_mask = int(line.strip().split()[-1], 16)
            return (led_mask & 0x02) != 0
    return False


# Global Variables
clicked_position = None
numlock_state = is_numlock_on()


def on_press(key):
    global numlock_state
    global clicked_position

    try:
        vk = getattr(key, "vk", None)
        char = getattr(key, "char", None)
        print(f"Key: {key}, VK: {vk}, Char: {char}")
    except Exception as e:
        print("Error:", e)

    if key == keyboard.Key.num_lock:
        numlock_state = not numlock_state
        print("Num Lock toggled:", "ON" if numlock_state else "OFF")
    print(f"vk: {vk}")
    vk = getattr(key, "vk", None)
    # print(f"vk: {vk}")
    if vk == 65437:
        print("Numpad 5 is pressed.")
        clicked_position = pyautogui.position()  # Get the XY position of the mouse
        print(f"clicked: {clicked_position}")
        pyautogui.click()
    if char == "/" and vk == None:
        # This will be left click 2
        print("Num / pressed")
    if char == "*" and vk == None:
        # This will be right click
        print("Num * pressed")


if __name__ == "__main__":
    print("NumLock is ON" if is_numlock_on() else "NumLock is OFF")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
