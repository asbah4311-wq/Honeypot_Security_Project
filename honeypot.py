import socket
import datetime
import json
import os

# Honeypot Configuration
HOST = '0.0.0.0'
PORTS = [21, 22, 23, 80, 3306]
LOG_FILE = 'honeypot_logs.json'

# Create log file if not exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

def log_attack(port, attacker_ip, data):
    # Read existing logs
    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)
    
    # Create new log entry
    entry = {
        "timestamp": str(datetime.datetime.now()),
        "attacker_ip": attacker_ip,
        "port_attacked": port,
        "service": get_service_name(port),
        "data_sent": data.decode('utf-8', errors='ignore')
    }
    
    # Save log entry
    logs.append(entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)
    
    print(f"[ATTACK DETECTED] {entry['timestamp']} | IP: {attacker_ip} | Port: {port} | Service: {entry['service']}")

def get_service_name(port):
    services = {
        21: 'FTP',
        22: 'SSH', 
        23: 'Telnet',
        80: 'HTTP',
        3306: 'MySQL'
    }
    return services.get(port, 'Unknown')

def handle_connection(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, port))
    server.listen(5)
    print(f"[HONEYPOT LISTENING] Port {port} ({get_service_name(port)})")
    
    while True:
        client, address = server.accept()
        attacker_ip = address[0]
        try:
            data = client.recv(1024)
            if data:
                log_attack(port, attacker_ip, data)
        except:
            pass
        finally:
            client.close()

# Start honeypot
print("=" * 50)
print("    HONEYPOT SYSTEM STARTED")
print("=" * 50)

import threading
for port in PORTS:
    thread = threading.Thread(target=handle_connection, args=(port,))
    thread.daemon = True
    thread.start()

print(f"Monitoring ports: {PORTS}")
print("Waiting for attacks...")
print("=" * 50)

# Keep running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nHoneypot stopped.")