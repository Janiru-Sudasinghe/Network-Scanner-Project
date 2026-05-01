import socket
import argparse
import ipaddress
import concurrent.futures

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0) 
    try:
        if s.connect_ex((str(ip), port)) == 0:
            print(f"[+] SUCCESS: {ip} Port {port} is OPEN!")
    except socket.error:
        pass 
    finally:
        s.close()

def parse_ports(port_str):
    """Hero Level: Parses both '22,80' and '1-1000' formats!"""
    ports = []
    for p in port_str.split(","):
        p = p.strip()
        if "-" in p:
            start, end = p.split("-")
            ports.extend(range(int(start), int(end) + 1)) # Gets all numbers in the range
        elif p:
            ports.append(int(p))
    return ports

def main():
    parser = argparse.ArgumentParser(description="Professional Network Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP or CIDR (e.g., 192.168.1.1)")
    parser.add_argument("-p", "--ports", default="21,22,23,80,139,443,445,3306,8080", help="Ports (e.g., 22,80 or 1-1000)")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Number of concurrent threads")
    
    args = parser.parse_args()
    
    # Use our new custom port parser
    ports = parse_ports(args.ports)
    
    try:
        network = ipaddress.ip_network(args.target, strict=False)
        
        print(f"Starting HIGH-SPEED scan on target(s): {args.target}")
        print(f"Scanning {len(ports)} ports using {args.workers} threads...")
        print("-" * 40)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            for ip in network.hosts():
                for port in ports:
                    executor.submit(scan_port, ip, port)
                    
        print("-" * 40)
        print("Scan complete!")
        
    except ValueError:
        print("[-] Error: Invalid IP address or CIDR block provided.")

if __name__ == "__main__":
    main()


# py scanner.py -t 192.168.120.131 -w 50   
# py scanner.py -t 192.168.120.131 -p 1-1000 -w 100