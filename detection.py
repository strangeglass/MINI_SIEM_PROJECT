# detection.py

import threading
import time
from config import BRUTE_FORCE_THRESHOLD, TIME_WINDOW
from database import get_db

attempts = {}
attempts_lock = threading.Lock()

def detect(ip, status):
    current_time = time.time()

    with attempts_lock:
        if ip not in attempts:
            attempts[ip] = []

        if status.upper() == "FAIL":
            attempts[ip].append(current_time)

            # Remove old attempts
            attempts[ip] = [t for t in attempts[ip] if current_time - t <= TIME_WINDOW]

            if len(attempts[ip]) >= BRUTE_FORCE_THRESHOLD:
                create_alert(ip)
                attempts[ip] = []

        elif status.upper() == "SUCCESS":
            attempts[ip] = []

def create_alert(ip):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (timestamp, ip, type)
        VALUES (datetime('now'), ?, ?)
    """, (ip, "Brute Force Detected"))

    conn.commit()
    conn.close()