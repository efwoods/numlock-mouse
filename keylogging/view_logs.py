# view_logs.py
import sqlite3
from cryptography.fernet import Fernet


def decrypt_logs(db_path="keystrokes.db", key_path="secret.key"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    with open(key_path, "rb") as f:
        key = f.read()
    fernet = Fernet(key)

    cur.execute("SELECT id, timestamp, key_encrypted FROM logs")
    rows = cur.fetchall()

    for row in rows:
        try:
            decrypted = fernet.decrypt(row[2].encode()).decode()
            print(f"{row[0]} | {decrypted}")
        except Exception as e:
            print(f"Decryption failed for row {row[0]}: {e}")

    conn.close()


if __name__ == "__main__":
    decrypt_logs()
