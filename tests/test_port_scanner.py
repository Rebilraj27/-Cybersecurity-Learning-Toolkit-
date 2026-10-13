"""
Tests for toolkit.port_scanner
"""

import socket
import threading

import pytest

from toolkit import port_scanner


class TestScanPort:

    def test_open_port_returns_true(self, listening_socket):
        srv, port = listening_socket
        assert port_scanner.scan_port("127.0.0.1", port) is True

    def test_closed_port_returns_false(self):
        assert port_scanner.scan_port("127.0.0.1", 1, timeout=0.3) is False

    def test_invalid_host_returns_false(self):
        assert port_scanner.scan_port("no.such.host.invalid", 80) is False

    def test_unroutable_ip_timeout(self):
        # 192.0.2.0/24 is TEST-NET-1 (reserved)
        assert port_scanner.scan_port("192.0.2.1", 80, timeout=0.2) is False


class TestGrabBanner:

    def test_banner_grabbed_from_service(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind(("127.0.0.1", 0))
        srv.listen(1)
        port = srv.getsockname()[1]

        def serve():
            conn, _ = srv.accept()
            conn.send(b"FAKE-BANNER-12345\r\n")
            conn.close()

        threading.Thread(target=serve, daemon=True).start()
        try:
            banner = port_scanner.grab_banner("127.0.0.1", port, timeout=2.0)
            assert "FAKE-BANNER" in banner
        finally:
            srv.close()

    def test_banner_on_closed_port(self):
        assert port_scanner.grab_banner("127.0.0.1", 1, timeout=0.3) == ""


class TestScan:

    def test_scan_finds_open_port(self, listening_socket):
        srv, port = listening_socket
        results = port_scanner.scan("127.0.0.1", [port], workers=5)
        assert port in [r[0] for r in results]

    def test_scan_empty_list(self):
        assert port_scanner.scan("127.0.0.1", []) == []

    def test_common_ports_mapping(self):
        assert port_scanner.COMMON_PORTS[80] == "HTTP"
        assert port_scanner.COMMON_PORTS[443] == "HTTPS"
        assert port_scanner.COMMON_PORTS[22] == "SSH"
        assert port_scanner.COMMON_PORTS[3306] == "MySQL"
