import socket

# 1. Define our target (your VM) and the port we want to check
TARGET_IP = "192.168.120.131"
PORT = 22  # Port 22 is for SSH, which we know is open on Metasploitable

def scan_port(ip, port):
    print(f"Attempting to scan {ip} on port {port}...")
    
    # 2. Create the socket (Think of this as creating our delivery van)
    # AF_INET means we are using IPv4, SOCK_STREAM means we are using TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 3. SET THE TIMEOUT! This is a strict requirement for your assignment.
    # If the port ignores us for 1 second, we move on instead of freezing.
    s.settimeout(1.0) 
    
    try:
        # 4. Try to connect. connect_ex() returns a '0' if the door is open.
        result = s.connect_ex((ip, port))
        
        if result == 0:
            print(f"[+] SUCCESS: Port {port} is OPEN!")
        else:
            print(f"[-] CLOSED: Port {port} is closed.")
            
    except socket.error as e:
        print(f"Network error occurred: {e}")
    finally:
        # 5. Always clean up and close the socket when done
        s.close()

# Run the function we just built
scan_port(TARGET_IP, PORT)