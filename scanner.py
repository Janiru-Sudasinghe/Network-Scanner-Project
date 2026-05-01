import socket

# 1. Define our target and a list of common ports to check
TARGET_IP = "192.168.120.131"
PORTS_TO_SCAN = [21, 22, 23, 80, 139, 443, 445, 3306, 8080]

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0) 
    
    try:
        result = s.connect_ex((ip, port))
        
        # We only print the open ports so our terminal doesn't get cluttered
        if result == 0:
            print(f"[+] SUCCESS: Port {port} is OPEN!")
            
    except socket.error:
        pass # If there is an error, just ignore it and move on
    finally:
        s.close()

print(f"Starting scan on target: {TARGET_IP}")
print("-" * 40) # Prints a nice dividing line

# 2. The Loop: Send the delivery van to every port in our list
for port in PORTS_TO_SCAN:
    scan_port(TARGET_IP, port)

print("-" * 40)
print("Scan complete!")