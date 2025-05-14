from pynput import keyboard


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


if __name__ == "__main__":
    combo = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char="k")}
    listener = KeyComboListener(combo)
    listener.start()

