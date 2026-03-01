import requests
import time
import json
import random
from datetime import datetime

# URL of the SIEM ingestion endpoint
URL = 'http://127.0.0.1:5000/ingest'

# Simulated IP addresses
ips = ['192.168.1.10', '10.0.0.5', '172.16.0.2', '203.0.113.45']

# Possible log messages
messages = [
    'User logged in successfully',
    'File accessed: /var/www/html/index.php',
    'Database connection established',
    'Failed password attempt for user: admin',
    'Failed password attempt for user: root',
    'New user created: guest'
]

def generate_log():
    """Generates a random log entry."""
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip': random.choice(ips),
        'message': random.choice(messages)
    }

def simulate_attack():
    """Simulates a sustained brute-force attack from a specific IP."""
    attacker_ip = '185.123.45.67'
    print(f"!!! Starting heavy simulation of brute-force attack from {attacker_ip} (1000 attempts) !!!")
    
    # Range set to 1000
    for i in range(1000): 
        log = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': attacker_ip,
            'message': f'Failed password attempt for user: admin (Attempt {i+1}/1000)'
        }
        send_log(log)
        # Reduced sleep to 0.05 seconds to send them faster
        time.sleep(0.05) 

def send_log(log):
    """Sends the log to the SIEM application."""
    try:
        response = requests.post(URL, json=log)
        if response.status_code == 200:
            print(f"Log sent: {log['ip']} - {log['message']}")
        else:
            print(f"Failed to send log: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the SIEM application. Is it running?")

if __name__ == '__main__':
    print("Starting SIEM Log Simulator...")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            # Randomly decide to run normal traffic or a brute-force simulation
            if random.random() < 0.1: # 10% chance to simulate an attack
                simulate_attack()
            else:
                log = generate_log()
                send_log(log)
            
            time.sleep(random.uniform(0.5, 2.0)) # Random delay between logs
    except KeyboardInterrupt:
        print("\nSimulator stopped.")