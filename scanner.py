"""
scanner.py — Network Discovery & Auditing Tool
===============================================
A high-performance, multi-threaded TCP port scanner for internal network auditing.

Course   : Python Programming – Network Programming Design
Group    : 08
Members  : COHNDNE251F-035 | COHNDNE251F-038 | COHNDNE251F-043 | COHNDNE251F-045

Usage:
    python scanner.py -t <target> [-p <ports>] [-w <workers>]

Examples:
    python scanner.py -t 192.168.1.1
    python scanner.py -t 192.168.1.0/24 -p 22,80,443
    python scanner.py -t 192.168.1.1 -p 1-1000 -w 100
"""

import socket
import argparse
import ipaddress
import concurrent.futures
import time
from typing import List


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_PORTS: str = "21,22,23,80,139,443,445,3306,8080"
DEFAULT_WORKERS: int = 50
DEFAULT_TIMEOUT: float = 1.0

# Common port-to-service name mappings for enriched output
SERVICE_NAMES: dict[int, str] = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    139:  "NetBIOS",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}


# ---------------------------------------------------------------------------
# Core Networking
# ---------------------------------------------------------------------------

def scan_port(ip_address: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Attempt a TCP connection to a single host/port combination.

    Opens a non-blocking socket, applies the specified timeout, and attempts
    a TCP handshake via ``connect_ex``. The socket is always closed in the
    ``finally`` block regardless of the outcome.

    Args:
        ip_address: The target IPv4 address as a string (e.g. ``"192.168.1.1"``).
        port:       The TCP port number to probe (1–65535).
        timeout:    Maximum seconds to wait for a connection (default: 1.0).

    Returns:
        A dictionary with keys:
            - ``ip``      (str)  : The scanned IP address.
            - ``port``    (int)  : The scanned port number.
            - ``open``    (bool) : ``True`` if the port accepted the connection.
            - ``service`` (str)  : Known service name, or ``"Unknown"`` if unmapped.
    """
    result = {
        "ip": ip_address,
        "port": port,
        "open": False,
        "service": SERVICE_NAMES.get(port, "Unknown"),
    }

    probe_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe_socket.settimeout(timeout)

    try:
        connection_result = probe_socket.connect_ex((ip_address, port))
        if connection_result == 0:
            result["open"] = True
    except socket.error:
        # Any socket-level error (e.g. network unreachable) is treated as
        # a closed / filtered port and suppressed to keep output clean.
        pass
    finally:
        probe_socket.close()

    return result


# ---------------------------------------------------------------------------
# Input Parsing
# ---------------------------------------------------------------------------

def parse_ports(port_string: str) -> List[int]:
    """Parse a flexible port specification string into a sorted list of integers.

    Accepts both comma-separated individual ports and hyphenated ranges.
    Mixed formats within the same string are supported.

    Args:
        port_string: A string such as ``"22,80,443"`` or ``"1-1024"``
                     or a combination like ``"22,80,1000-1010"``.

    Returns:
        A sorted list of unique integer port numbers.

    Raises:
        ValueError: If any token cannot be converted to a valid integer,
                    or if a range has its bounds in the wrong order.

    Examples:
        >>> parse_ports("22,80,443")
        [22, 80, 443]
        >>> parse_ports("1-5")
        [1, 2, 3, 4, 5]
        >>> parse_ports("21,80,100-102")
        [21, 80, 100, 101, 102]
    """
    port_list: List[int] = []

    for token in port_string.split(","):
        token = token.strip()
        if not token:
            continue

        if "-" in token:
            parts = token.split("-", 1)
            range_start = int(parts[0].strip())
            range_end = int(parts[1].strip())

            if range_start > range_end:
                raise ValueError(
                    f"Invalid port range '{token}': start must be <= end."
                )

            port_list.extend(range(range_start, range_end + 1))
        else:
            port_list.append(int(token))

    # Deduplicate and sort for deterministic, readable output
    return sorted(set(port_list))


def parse_target(target_string: str) -> ipaddress.IPv4Network:
    """Parse a target string into an IPv4Network object.

    Accepts both a single host address (``"192.168.1.1"``) and CIDR
    notation (``"192.168.1.0/24"``). The ``strict=False`` flag permits
    host bits to be set in CIDR notation without raising an error.

    Args:
        target_string: An IPv4 address or CIDR block string.

    Returns:
        An :class:`ipaddress.IPv4Network` instance representing the target.

    Raises:
        ValueError: If ``target_string`` is not a valid IPv4 address or network.
    """
    return ipaddress.ip_network(target_string, strict=False)


# ---------------------------------------------------------------------------
# Output Formatting
# ---------------------------------------------------------------------------

def print_banner(target: str, port_count: int, worker_count: int) -> None:
    """Print the scan header banner to stdout.

    Args:
        target:       The original target string supplied by the user.
        port_count:   Total number of ports that will be scanned per host.
        worker_count: Number of concurrent threads configured for the scan.
    """
    separator = "=" * 56
    print(f"\n{separator}")
    print("     Network Discovery & Auditing Tool — Group 08")
    print(separator)
    print(f"  Target  : {target}")
    print(f"  Ports   : {port_count} port(s) queued")
    print(f"  Threads : {worker_count} concurrent workers")
    print(f"{separator}\n")


def print_open_port(result: dict) -> None:
    """Print a formatted line for a confirmed open port.

    Args:
        result: The result dictionary returned by :func:`scan_port`.
    """
    service_label = f"({result['service']})" if result["service"] != "Unknown" else ""
    print(f"  [OPEN]  {result['ip']:<18} Port {result['port']:<6} {service_label}")


def print_summary(open_count: int, total_checks: int, elapsed: float) -> None:
    """Print the post-scan summary to stdout.

    Args:
        open_count:   Number of open ports discovered.
        total_checks: Total number of port checks performed.
        elapsed:      Wall-clock time taken for the scan in seconds.
    """
    separator = "=" * 56
    print(f"\n{separator}")
    print(f"  Scan complete.")
    print(f"  Open ports found : {open_count}")
    print(f"  Total checks     : {total_checks}")
    print(f"  Time elapsed     : {elapsed:.2f} seconds")
    print(f"{separator}\n")


# ---------------------------------------------------------------------------
# Scan Orchestration
# ---------------------------------------------------------------------------

def run_scan(
    target_string: str,
    port_string: str,
    worker_count: int,
) -> None:
    """Orchestrate a full multi-threaded network scan.

    Parses the target and port inputs, dispatches concurrent TCP probes
    using a :class:`concurrent.futures.ThreadPoolExecutor`, collects all
    results, and prints a formatted summary upon completion.

    Args:
        target_string: Raw target input from the CLI (IP or CIDR).
        port_string:   Raw port specification from the CLI.
        worker_count:  Number of threads to use for concurrent scanning.
    """
    try:
        network = parse_target(target_string)
    except ValueError as error:
        print(f"\n  [ERROR] Invalid target — {error}")
        return

    try:
        ports = parse_ports(port_string)
    except ValueError as error:
        print(f"\n  [ERROR] Invalid port specification — {error}")
        return

    hosts = list(network.hosts()) if network.num_addresses > 1 else [network.network_address]

    print_banner(target_string, len(ports), worker_count)

    open_port_count = 0
    total_checks = len(hosts) * len(ports)
    futures_map = {}

    start_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        for host in hosts:
            for port in ports:
                future = executor.submit(scan_port, str(host), port)
                futures_map[future] = (str(host), port)

        for future in concurrent.futures.as_completed(futures_map):
            try:
                result = future.result()
                if result["open"]:
                    open_port_count += 1
                    print_open_port(result)
            except Exception as error:
                host, port = futures_map[future]
                print(f"  [WARN]  Unexpected error scanning {host}:{port} — {error}")

    elapsed_time = time.perf_counter() - start_time
    print_summary(open_port_count, total_checks, elapsed_time)


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def build_argument_parser() -> argparse.ArgumentParser:
    """Construct and return the CLI argument parser.

    Returns:
        A configured :class:`argparse.ArgumentParser` instance.
    """
    parser = argparse.ArgumentParser(
        prog="scanner.py",
        description=(
            "Network Discovery & Auditing Tool — Group 08\n"
            "Performs multi-threaded TCP port scanning across single hosts or CIDR subnets."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scanner.py -t 192.168.1.1\n"
            "  python scanner.py -t 192.168.1.0/24 -p 22,80,443\n"
            "  python scanner.py -t 192.168.1.1 -p 1-1000 -w 100\n\n"
            "Disclaimer:\n"
            "  Use only on networks for which you have explicit authorisation."
        ),
    )

    parser.add_argument(
        "-t", "--target",
        required=True,
        metavar="TARGET",
        help="Target IPv4 address or CIDR block (e.g., 192.168.1.1 or 192.168.1.0/24)",
    )
    parser.add_argument(
        "-p", "--ports",
        default=DEFAULT_PORTS,
        metavar="PORTS",
        help=(
            "Ports to scan. Accepts comma-separated values or ranges "
            f"(default: {DEFAULT_PORTS})"
        ),
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        metavar="WORKERS",
        help=f"Number of concurrent threads (default: {DEFAULT_WORKERS})",
    )

    return parser


def main() -> None:
    """Parse CLI arguments and initiate the network scan."""
    parser = build_argument_parser()
    args = parser.parse_args()

    run_scan(
        target_string=args.target,
        port_string=args.ports,
        worker_count=args.workers,
    )


if __name__ == "__main__":
    main()