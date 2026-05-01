import socket
import argparse
import ipaddress

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0) 
    try:
        # We wrap 'ip' in str() because the ipaddress module creates objects, but socket needs a string
        if s.connect_ex((str(ip), port)) == 0:
            print(f"[+] SUCCESS: {ip} Port {port} is OPEN!")
    except socket.error:
        pass 
    finally:
        s.close()

def main():
    # 1. Set up the CLI Interface (argparse)
    parser = argparse.ArgumentParser(description="Professional Network Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP or CIDR (e.g., 192.168.1.1 or 192.168.1.0/24)")
    parser.add_argument("-p", "--ports", default="21,22,23,80,139,443,445,3306", help="Comma-separated ports")
    
    args = parser.parse_args()
    
    # Convert the string of ports "22,80" into a list of numbers [22, 80]
    ports = [int(p.strip()) for p in args.ports.split(",")]
    
    try:
        # 2. Set up Subnet Parsing (ipaddress)
        # This magically handles both single IPs and full /24 subnets!
        network = ipaddress.ip_network(args.target, strict=False)
        
        print(f"Starting scan on target(s): {args.target}")
        print("-" * 40)
        
        # Loop through every IP in the subnet (or just loop once if it's a single IP)
        for ip in network.hosts():
            for port in ports:
                scan_port(ip, port)
                
        print("-" * 40)
        print("Scan complete!")
        
    except ValueError:
        print("[-] Error: Invalid IP address or CIDR block provided.")

# This ensures the main() function runs when we start the script
if __name__ == "__main__":
    main()



# py scanner.py -t 192.168.120.131