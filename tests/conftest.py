"""
conftest.py
===========
Shared pytest fixtures for Cyber Toolkit tests.

Created by: Rebilraj
"""

import os
import sys
import socket
import threading
import http.server
import socketserver

import pytest

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# ─────────────────────────────────────────────────────────────
#  Wordlist Fixture
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def sample_wordlist(tmp_path):
    """Create a small temporary wordlist for hash-cracker tests."""
    words = [
        "hello", "world", "password", "admin", "letmein",
        "secret", "qwerty", "abc123", "rebilraj", "cyber",
        "test123", "welcome", "monkey", "dragon", "master",
    ]
    wl = tmp_path / "wordlist.txt"
    wl.write_text("\n".join(words), encoding="utf-8")
    return str(wl)


# ─────────────────────────────────────────────────────────────
#  Local HTTP Server Fixture
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def local_http_server():
    """
    Spin up a tiny HTTP server on a random port to test the web scanner.
    Yields the base URL. Tears down automatically.
    """
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            # Deliberately missing security headers for testing
            self.end_headers()
            body = f"<html><body>Query: {self.path}</body></html>"
            self.wfile.write(body.encode())

        def log_message(self, *args, **kwargs):
            pass  # silence logs

    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as httpd:
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{port}"
        finally:
            httpd.shutdown()


# ─────────────────────────────────────────────────────────────
#  Free Port Fixture (for port scanner tests)
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def free_port():
    """Return an OS-assigned free TCP port on localhost."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture
def listening_socket():
    """Context-managed listening socket on a random port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    try:
        yield s, s.getsockname()[1]
    finally:
        s.close()


# ─────────────────────────────────────────────────────────────
#  Temp File Fixture
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def temp_file(tmp_path):
    """Return a factory that creates a temp file with given content."""
    def _make(content: str, name: str = "temp.txt"):
        f = tmp_path / name
        f.write_text(content, encoding="utf-8")
        return str(f)
    return _make


# ─────────────────────────────────────────────────────────────
#  Scapy Packet Fixtures
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def scapy_packets():
    """Build a dict of pre-made Scapy packets for sniffer tests."""
    scapy = pytest.importorskip("scapy.all")
    return {
        "tcp_syn": scapy.Ether() / scapy.IP(src="10.0.0.1", dst="10.0.0.2")
                   / scapy.TCP(sport=12345, dport=80, flags="S"),
        "tcp_https": scapy.Ether() / scapy.IP(src="10.0.0.1", dst="10.0.0.2")
                     / scapy.TCP(sport=50000, dport=443),
        "udp_dns": scapy.Ether() / scapy.IP(src="10.0.0.1", dst="8.8.8.8")
                   / scapy.UDP(sport=53000, dport=53)
                   / scapy.DNS(rd=1, qd=scapy.DNSQR(qname=b"example.com")),
        "icmp": scapy.Ether() / scapy.IP(src="10.0.0.1", dst="10.0.0.2")
                / scapy.ICMP(),
        "arp": scapy.Ether() / scapy.ARP(psrc="10.0.0.1", pdst="10.0.0.2"),
        "http_payload": scapy.IP(src="1.1.1.1", dst="2.2.2.2")
                        / scapy.TCP(sport=1000, dport=80)
                        / scapy.Raw(load=b"GET / HTTP/1.1\r\nHost: example.com"),
    }
