# Project: Inventory Tracking and Management System
# Author: Ali Zubair Shah
# GitHub: https://github.com/K3rNel1
import random
import sqlite3
import os
import hashlib
import base64

DB_FILE = "passwords.db"

def _get_conn():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS passwords (key TEXT PRIMARY KEY, password TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS auth (id INTEGER PRIMARY KEY, question TEXT, answer_hash TEXT)"
    )
    conn.commit()
    return conn


_ENC_KEY = "K3rNel_AliZubairShah_2024"

def encrypt_password(plain):
    key = _ENC_KEY
    enc = []
    for i, ch in enumerate(plain):
        enc.append(chr(ord(ch) ^ ord(key[i % len(key)])))
    return base64.b64encode("".join(enc).encode()).decode()

def decrypt_password(cipher):
    key = _ENC_KEY
    try:
        decoded = base64.b64decode(cipher.encode()).decode()
    except Exception:
        return cipher
    dec = []
    for i, ch in enumerate(decoded):
        dec.append(chr(ord(ch) ^ ord(key[i % len(key)])))
    return "".join(dec)


_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#!$&"

def generate_password(length=8):
    return "".join(random.choice(_CHARS) for _ in range(length))


def add_entry(key, password):
    conn = _get_conn()
    try:
        encrypted = encrypt_password(password)
        conn.execute(
            "INSERT OR REPLACE INTO passwords (key, password) VALUES (?, ?)",
            (key, encrypted),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_entries():
    conn = _get_conn()
    try:
        rows = conn.execute("SELECT key, password FROM passwords").fetchall()
        return rows
    finally:
        conn.close()

def update_entry(key, new_password):
    conn = _get_conn()
    try:
        encrypted = encrypt_password(new_password)
        conn.execute(
            "REPLACE INTO passwords (key, password) VALUES (?, ?)",
            (key, encrypted),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def delete_entry(key):
    conn = _get_conn()
    try:
        conn.execute("DELETE FROM passwords WHERE key = ?", (key,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def _hash(text):
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()

def setup_security_question(question, answer):
    conn = _get_conn()
    try:
        conn.execute("DELETE FROM auth")
        conn.execute(
            "INSERT INTO auth (question, answer_hash) VALUES (?, ?)",
            (question, _hash(answer)),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_security_question():
    conn = _get_conn()
    try:
        row = conn.execute("SELECT question FROM auth").fetchone()
        return row[0] if row else None
    finally:
        conn.close()

def verify_security_answer(answer):
    conn = _get_conn()
    try:
        row = conn.execute("SELECT answer_hash FROM auth").fetchone()
        if not row:
            return True
        return _hash(answer) == row[0]
    finally:
        conn.close()

def auth_configured():
    conn = _get_conn()
    try:
        row = conn.execute("SELECT id FROM auth").fetchone()
        return row is not None
    finally:
        conn.close()


def main():
    os.system('attrib +h passwords.db')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS passwords (key TEXT PRIMARY KEY, password TEXT)")

    chars = _CHARS

    print("----------------------------------------------------------------------------")
    print("\n Welcome to Password Manager!\n")
    print("1 : Generate password")
    print("2 : Save your own password")
    print("3 : Saved passwords")
    print("4 : Update saved passwords")

    option = int(input("\n [1/2/3/4] : "))

    if option == 3:
        cursor.execute("SELECT * FROM passwords")
        rows = cursor.fetchall()
        if rows:
            print("\n Saved passwords:")
            for key, pwd in rows:
                print(f"\n Key: {key}, Password: {pwd}")

            opt = input("\n Do you want to delete any password? [y/n] : ").lower()
            if opt == "n":
                print("\n Task Completed \n")
            elif opt == "y":
                key = input("\n Enter the key of the password to delete: ")
                cursor.execute("DELETE FROM passwords WHERE key = ?", (key,))
                conn.commit()
                print("\n password for", key, "deleted.")
            else:
                print("\n Invalid option\n")
        else:
            print("\n No passwords saved\n")

    if option == 1:
        password = ""
        length = int(input("\n Enter the length of required password : "))
        for i in range(length):
            password += random.choice(chars)

        print("\n Generated password : ", password)
        sav = input("\n Do you want to save this password [y/n] : ").lower()

        if sav == "n":
            print("\n Task Completed\n")
        elif sav == "y":
            key = input("\n Enter a key for the password : ")
            cursor.execute(
                "INSERT OR REPLACE INTO passwords (key, password) VALUES (?, ?)",
                (key, password),
            )
            conn.commit()
            print("\n Password for", key, "saved")
        else:
            print("\n Invalid Option\n")

    if option == 2:
        key = input("\n Enter a key for the password : ")
        password = input("\n Enter the password : ")
        cursor.execute(
            "INSERT OR REPLACE INTO passwords (key, password) VALUES (?, ?)",
            (key, password),
        )
        conn.commit()
        print("\n Password for", key, "saved")

    if option == 4:
        cursor.execute("SELECT * FROM passwords")
        rows = cursor.fetchall()
        if rows:
            for key, pwd in rows:
                print(f"\n Key: {key}, Password: {pwd}")

            key = input("\n Enter the key of the password : ")
            password = input("\n Enter the updated password : ")
            cursor.execute(
                "REPLACE INTO passwords (key, password) VALUES (?, ?)",
                (key, password),
            )
            conn.commit()
            print("\n Password for", key, "updated to", password)
        else:
            print("\n No passwords saved\n")
    conn.close()


if __name__ == "__main__":
    if not auth_configured():
        print("\n --- Create Account ---")
        q = input(" Enter a security question: ")
        a = input(" Enter the answer: ")
        setup_security_question(q, a)
        print(" Account created successfully!\n")
    else:
        q = get_security_question()
        print(f"\n Security Question: {q}")
        a = input(" Answer: ")
        if not verify_security_answer(a):
            print(" Incorrect answer. Exiting.")
            exit(0)
        print(" Login successful!\n")

    while True:
        main()
