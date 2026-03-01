import requests
import time
from datetime import datetime
import random

# The URL of our SIEM ingestion endpoint
URL = "http://127.0.0.1:5000/ingest"

def send_log(ip, message):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": ip,
        "message": message
    }
    try:
        response = requests.post(URL, json=log_entry)
        print(f"Sent: {ip} - {message} | Response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send log: {e}")

if __name__ == "__main__":
    attacker_ip = "192.168.1.100"
    
    print("Starting attack simulation...")
    
    # Send 5 failed login attempts quickly
    for i in range(5):
        send_log(attacker_ip, "SSH login failed")
        time.sleep(1) # Wait 1 second between attempts
        
    print("Simulation finished.")