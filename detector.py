import sqlite3
from datetime import datetime, timedelta
import config  # Import our security rules

def check_for_brute_force(ip_address):
    """
    Checks if a specific IP address has exceeded the failure threshold 
    within the defined time window.
    """
    conn = sqlite3.connect('siem.db')
    cursor = conn.cursor()
    
    # Calculate the time window (e.g., 60 seconds ago)
    time_limit = datetime.now() - timedelta(seconds=config.TIME_WINDOW)
    
    # Count failed attempts in the window
    cursor.execute('''
        SELECT COUNT(*) FROM logs 
        WHERE ip = ? AND message LIKE '%failed%' AND timestamp > ?
    ''', (ip_address, time_limit))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    # Check if threshold is exceeded
    if count >= config.FAILURE_THRESHOLD:
        print(f"Brute force detected from {ip_address}: {count} failures")
        return True
    
    return False