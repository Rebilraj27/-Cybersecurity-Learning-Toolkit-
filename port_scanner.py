import socket
import concurrent.futures
from rich.console import Console
from rich.table import Table

console = Console()

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt"
}

def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Return True if port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except socket.error:
        return False

def grab_banner(host: str, port: int, timeout: float = 1.0) -> str:
    """Attempt to grab a service banner."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            s.send(b"\r\n")
            return s.recv(1024).decode(errors="ignore").strip()[:60]
    except Exception:
        return ""

def scan(host: str, ports: list[int], workers: int = 100):
    console.print(f"[bold cyan]Scanning {host}...[/]")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(scan_port, host, p): p for p in ports}
        for f in concurrent.futures.as_completed(futures):
            port = futures[f]
            if f.result():
                banner = grab_banner(host, port)
                results.append((port, COMMON_PORTS.get(port, "unknown"), banner))

    table = Table(title=f"Open Ports on {host}")
    table.add_column("Port", style="green")
    table.add_column("Service", style="yellow")
    table.add_column("Banner", style="white")
    for port, svc, banner in sorted(results):
        table.add_row(str(port), svc, banner or "-")
    console.print(table)
    return results
