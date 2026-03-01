# simulator.py
import requests
import time
import random
from datetime import datetime

# URL of the SIEM ingestion endpoint
URL = 'http://127.0.0.1:5000/ingest'

# Simulated IP addresses
ips = ['192.168.1.10', '10.0.0.5', '172.16.0.2', '203.0.113.45']

# Possible status messages for normal logs
statuses = ['SUCCESS', 'SUCCESS', 'SUCCESS', 'FAIL']

def generate_log():
    """Generates a random log entry matching the format: timestamp ip status"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip = random.choice(ips)
    status = random.choice(statuses)
    
    # Format according to routes.py requirements
    return f"{timestamp} {ip} {status}"

def simulate_attack():
    """Simulates a sustained brute-force attack from a specific IP."""
    attacker_ip = '185.123.45.67'
    print(f"!!! Starting heavy simulation of brute-force attack from {attacker_ip} !!!")
    
    # Send multiple fail attempts rapidly
    for i in range(10): 
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"{timestamp} {attacker_ip} FAIL"
        
        send_log(log_line)
        time.sleep(0.1) # Fast attempts

def send_log(log_string):
    """Sends the log to the SIEM application using form data."""
    try:
        # routes.py expects request.form.get("log")
        payload = {'log': log_string}
        response = requests.post(URL, data=payload)
        
        if response.status_code == 200:
            print(f"Log sent: {log_string}")
        else:
            print(f"Failed to send log: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the SIEM application. Is it running?")

if __name__ == '__main__':
    print("Starting SIEM Log Simulator...")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            # Randomly decide to run normal traffic or a brute-force simulation
            if random.random() < 0.2: # 20% chance to simulate an attack
                simulate_attack()
            else:
                log = generate_log()
                send_log(log)
            
            time.sleep(random.uniform(0.5, 1.5)) # Delay between actions
    except KeyboardInterrupt:
        print("\nSimulator stopped.")