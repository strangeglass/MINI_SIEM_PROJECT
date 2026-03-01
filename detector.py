import sqlite3
from datetime import datetime, timedelta

def check_for_brute_force(ip_address):
    conn = sqlite3.connect('siem.db')
    cursor = conn.cursor()
    
    # This is where we will check for failures in the last 60 seconds
    # For now, just a placeholder for the logic
    print(f"Checking IP: {ip_address}")
    
    conn.close()
    return False # No alert yet