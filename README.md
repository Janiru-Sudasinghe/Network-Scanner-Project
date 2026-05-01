# Network Scanner Project - Group 08

## Group Member 
Index No - COHNDNE251F-035
Index No - COHNDNE251F-038
Index No - COHNDNE251F-043
Index No - COHNDNE251F-045

## Scenario
This tool was developed for internal auditing as a high-performance Network Scanner. It is designed to be faster than basic scripts, handle network errors gracefully, and provide a professional command-line experience.

## Features
* **Core Networking:** Utilizes the `socket` module with customized timeouts to prevent hanging on filtered ports.
* **Subnet Parsing:** Integrates the `ipaddress` module to support single IP targeting or full CIDR block scanning (e.g., 192.168.1.0/24).
* **High Performance:** Uses `concurrent.futures.ThreadPoolExecutor` for multi-threaded scanning, drastically reducing scan times.
* **CLI Interface:** Built with `argparse` for a flexible, user-friendly terminal experience.

## Setup Instructions
1. Ensure Python 3.x is installed on your system.
2. No external libraries are required (only Python standard libraries are used).
3. Clone or download this repository.

## Usage Examples

**Basic Scan (Default Ports):**
`python scanner.py -t 192.168.1.1`

**Scan a Subnet for Specific Ports:**
`python scanner.py -t 192.168.1.0/24 -p 22,80,443`

**High-Speed Scan (Custom Thread Count & Port Range):**
`python scanner.py -t 192.168.1.1 -p 1-1000 -w 100`

## Arguments
* `-t` / `--target` : (Required) Target IP or CIDR block.
* `-p` / `--ports`  : (Optional) Comma-separated ports or ranges (default: 21,22,23,80,139,443,445,3306,8080).
* `-w` / `--workers`: (Optional) Number of concurrent threads (default: 50).