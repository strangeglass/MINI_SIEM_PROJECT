import sqlite3
from datetime import datetime, timedelta
import config  # Import our security rules

def check_for_brute_force(ip_address):
    """
    Checks if a specific IP address has exceeded the failure threshold 
    within the defined time window. If true, saves an alert to the database.
    """
    conn = sqlite3.connect('siem.db')
    cursor = conn.cursor()
    
    # Calculate the time window
    time_limit = datetime.now() - timedelta(seconds=config.TIME_WINDOW)
    
    # Count failed attempts in the window
    cursor.execute('''
        SELECT COUNT(*) FROM logs 
        WHERE ip = ? AND message LIKE '%failed%' AND timestamp > ?
    ''', (ip_address, time_limit))
    
    count = cursor.fetchone()[0]
    
    # Check if threshold is exceeded
    if count >= config.FAILURE_THRESHOLD:
        print(f"Brute force detected from {ip_address}: {count} failures")
        
        # NEW: Save the alert to the database
        cursor.execute('''
            INSERT INTO alerts (timestamp, ip, reason) 
            VALUES (?, ?, ?)
        ''', (datetime.now(), ip_address, f"Brute Force: {count} failed logins"))
        conn.commit()
        
        conn.close()
        return True
    
    conn.close()
    return False