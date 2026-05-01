# 🔍 Network Discovery & Auditing Tool

> A high-performance, multi-threaded Python network scanner built for internal auditing. Developed as part of the Python Programming – Network Programming Design coursework.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Threading](https://img.shields.io/badge/Threading-concurrent.futures-orange?style=flat-square)
![CLI](https://img.shields.io/badge/CLI-argparse-purple?style=flat-square)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Group Members](#group-members)
- [Technical Architecture](#technical-architecture)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [CLI Reference](#cli-reference)
- [Development Phases](#development-phases)
- [Project Structure](#project-structure)
- [Acknowledgements](#acknowledgements)

---

## Project Overview

**Scenario:** As part of a simulated Junior Security Engineer role at a cybersecurity firm, this tool was developed to fulfil the requirement for a professional-grade network scanner capable of conducting internal audits across enterprise subnets.

The scanner is engineered to outperform basic scripting solutions by leveraging concurrent multi-threading, robust error handling, and a structured command-line interface. It identifies open TCP ports across single hosts or full CIDR blocks, making it suitable for both targeted and broad-spectrum auditing tasks.

This project demonstrates mastery of **Socket Programming**, **Concurrency**, and **Input Parsing** as outlined in the assignment brief.

---

## Group Members

| Index Number       | Contribution |
|--------------------|--------------|
| COHNDNE251F-035    | Core Networking & Socket Implementation |
| COHNDNE251F-038    | Subnet Parsing & IP Address Module Integration |
| COHNDNE251F-043    | Multi-threading Architecture & Performance Optimisation |
| COHNDNE251F-045    | CLI Interface, Argument Parsing & Documentation |

> **Repository:** [Network-Scanner-Project](https://github.com/Janiru-Sudasinghe/Network-Scanner-Project)
> All group members have maintained an active commit history to reflect individual contributions throughout the development lifecycle.

---

## Technical Architecture

The tool is structured around four core development phases, each building upon the last to deliver a production-quality scanning solution:

```
User Input (argparse)
       │
       ▼
  IP / CIDR Parsing (ipaddress module)
       │
       ▼
 ThreadPoolExecutor (concurrent.futures)
   ┌───┴───────────────────┐
   │   Thread 1            │  Thread N
   │   socket.connect()    │  socket.connect()
   │   → Port Result       │  → Port Result
   └───────────────────────┘
       │
       ▼
  Aggregated Results → Terminal Output
```

---

## Key Features

| Feature | Description | Module Used |
|---|---|---|
| **Core Networking** | Attempts TCP connections with configurable timeouts to prevent hanging on filtered ports | `socket` |
| **Subnet Parsing** | Supports scanning of a single IP or a full CIDR block (e.g., `192.168.1.0/24`) | `ipaddress` |
| **High Performance** | Multi-threaded architecture reduces scan time dramatically over sequential approaches | `concurrent.futures.ThreadPoolExecutor` |
| **CLI Interface** | Flexible terminal interface supporting target, port range, and thread count configuration | `argparse` |
| **Error Handling** | Gracefully manages unreachable hosts, refused connections, and network timeouts | `socket`, `try/except` |

---

## Requirements

- **Python 3.x** (no version below 3.4 supported due to `ipaddress` and `concurrent.futures`)
- **No external dependencies** — the tool is built entirely on the Python Standard Library

```
socket
ipaddress
concurrent.futures
argparse
```

---

## Installation & Setup

**Step 1 — Clone the repository**

```bash
git clone https://github.com/Janiru-Sudasinghe/Network-Scanner-Project
cd Network-Scanner-Project
```

**Step 2 — Verify Python version**

```bash
python --version
# Expected: Python 3.x
```

**Step 3 — Confirm no external packages are needed**

```bash
# No pip install required. All modules are from the Python Standard Library.
```

---

## Usage

### Basic Scan — Single Host (Default Ports)

Scans a single IP address using the default set of commonly audited ports.

```bash
py scanner.py -t 192.168.120.131
```

**Default ports scanned:** `21, 22, 23, 80, 139, 443, 445, 3306, 8080`

---

### Subnet Scan — CIDR Block with Specific Ports

Scans all hosts in a `/24` subnet for specified ports, useful for broad internal audits.

```bash
py scanner.py -t 192.168.120.0/24 -p 22,80,443
```

---

### Port Range Scan — Custom Range with Increased Thread Count

Scans a range of ports on a single host using 100 concurrent threads for maximum throughput.

```bash
py scanner.py -t 192.168.120.131 -p 1-1000 -w 100
```

---

### Mixed Format — Individual Ports and Range

Combines individual port declarations with a hyphenated range.

```bash
py scanner.py -t 192.168.120.131 -p 21,22,80,8000-8010 -w 75
```

---

### Error Case — Malformed Target

Tests error handling by providing an invalid IP address (gracefully prints a clean error without crashing).

```bash
python scanner.py -t not-an-ip -p 80
```

---

### Sample Output

```bash
py scanner.py -t 192.168.120.131 -p 1-1000 -w 100
```

```
========================================================
     Network Discovery & Auditing Tool — Group 08
========================================================
  Target  : 192.168.120.131
  Ports   : 1000 port(s) queued
  Threads : 100 concurrent workers
========================================================

  [OPEN]  192.168.120.131    Port 53     (DNS)
  [OPEN]  192.168.120.131    Port 23     (Telnet)
  [OPEN]  192.168.120.131    Port 25     (SMTP)
  [OPEN]  192.168.120.131    Port 80     (HTTP)
  [OPEN]  192.168.120.131    Port 22     (SSH)
  [OPEN]  192.168.120.131    Port 21     (FTP)
  [OPEN]  192.168.120.131    Port 139    (NetBIOS)
  [OPEN]  192.168.120.131    Port 111    
  [OPEN]  192.168.120.131    Port 445    (SMB)
  [OPEN]  192.168.120.131    Port 513    
  [OPEN]  192.168.120.131    Port 512    
  [OPEN]  192.168.120.131    Port 514    

========================================================
  Scan complete.
  Open ports found : 12
  Total checks     : 1000
  Time elapsed     : 10.16 seconds
========================================================
```

---

## CLI Reference

| Argument | Long Form | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `-t` | `--target` | `str` | ✅ Yes | — | Target IP address or CIDR subnet block |
| `-p` | `--ports` | `str` | ❌ No | `21,22,23,80,139,443,445,3306,8080` | Comma-separated ports or a range (e.g., `1-1024`) |
| `-w` | `--workers` | `int` | ❌ No | `50` | Number of concurrent threads to use during scan |

**Full help output:**

```bash
py scanner.py --help
```

```
usage: scanner.py [-h] -t TARGET [-p PORTS] [-w WORKERS]

Network Discovery & Auditing Tool — Group 08
Performs multi-threaded TCP port scanning across single hosts or CIDR subnets.

options:
  -h, --help            show this help message and exit
  -t, --target TARGET   Target IPv4 address or CIDR block (e.g., 192.168.1.1 or 192.168.1.0/24)
  -p, --ports PORTS     Ports to scan. Accepts comma-separated values or ranges (default: 21,22,23,80,139,443,445,3306,8080)
  -w, --workers WORKERS
                        Number of concurrent threads (default: 50)

Examples:
  python scanner.py -t 192.168.1.1
  python scanner.py -t 192.168.1.0/24 -p 22,80,443
  python scanner.py -t 192.168.1.1 -p 1-1000 -w 100

Disclaimer:
  Use only on networks for which you have explicit authorisation.
```

---

## Development Phases

This project was developed across five structured phases as specified in the assignment brief:

### Phase 1 — Core Networking
Implemented TCP connection attempts using the `socket` module. Each connection is subject to a configurable timeout to ensure the scanner does not hang indefinitely on filtered or unresponsive ports.

### Phase 2 — Subnet Parsing
Integrated the `ipaddress` module to allow the tool to accept both single IP addresses and CIDR notation. All host addresses within a given block are enumerated and scanned systematically.

### Phase 3 — High-Performance Multi-threading
Replaced the initial synchronous scan loop with a `concurrent.futures.ThreadPoolExecutor`. This enables hundreds of port checks to occur simultaneously, reducing scan times by orders of magnitude compared to sequential execution.

### Phase 4 — CLI Interface
Built a professional command-line interface using `argparse`. Users can specify all scan parameters directly at the terminal without modifying source code, supporting flexible and repeatable audit workflows.

### Phase 5 — Version Control & Collaboration
The project was managed through a GitHub repository named **Network-Scanner-Project**. All group members contributed via individual commits, ensuring a traceable and verifiable development history. The repository includes full documentation and setup instructions.

- 🔗 **Repository:** [https://github.com/your-group/Network-Scanner-Project](https://github.com/Janiru-Sudasinghe/Network-Scanner-Project)

---

## Project Structure

```
Network-Scanner-Project/
│
├── scanner.py          # Main source file — all scanning logic
├── README.md           # Project documentation (this file)
└── requirements.txt    # Dependency declaration (standard library only)
```

---

## Ethical & Legal Disclaimer

> ⚠️ **This tool is intended for authorised use only.**
> Scanning networks or systems without explicit permission is illegal and unethical. This tool was developed solely for academic purposes within a controlled lab environment. The authors and contributors accept no liability for misuse.

---

## Acknowledgements

- Developed as a submission for **Python Programming – Network Programming Design**
- Course Institution: *National Institute of Business Management (NIBM)*
- Submitted by: **Group 08**
- Due: Sunday, 3 May 2026