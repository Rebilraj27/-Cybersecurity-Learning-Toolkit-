"""
Tests for toolkit.web_vuln_scanner
Uses the local HTTP server fixture — no external network required.
"""

import pytest

from toolkit import web_vuln_scanner


class TestCheckHeaders:

    def test_missing_headers_flagged(self, local_http_server):
        issues = web_vuln_scanner.check_headers(local_http_server)
        assert any("CSP" in i or "Content-Security-Policy" in i for i in issues)
        assert any("X-Frame-Options" in i for i in issues)

    def test_unreachable_url(self):
        issues = web_vuln_scanner.check_headers("http://127.0.0.1:1")
        assert len(issues) >= 1
        assert any("failed" in i.lower() or "request" in i.lower() for i in issues)


class TestReflectedXSS:

    def test_reflected_xss_detected(self, local_http_server):
        url = f"{local_http_server}/?q=test"
        assert web_vuln_scanner.test_reflected_xss(url) is True

    def test_no_params_returns_false(self, local_http_server):
        assert web_vuln_scanner.test_reflected_xss(local_http_server) is False


class TestScan:

    def test_scan_returns_expected_keys(self, local_http_server):
        result = web_vuln_scanner.scan(local_http_server + "/?q=x")
        assert "url" in result
        assert "header_issues" in result
        assert "possible_reflected_xss" in result

    def test_scan_url_echoed(self, local_http_server):
        url = local_http_server + "/?q=x"
        assert web_vuln_scanner.scan(url)["url"] == url

    def test_scan_types(self, local_http_server):
        result = web_vuln_scanner.scan(local_http_server)
        assert isinstance(result["header_issues"], list)
        assert isinstance(result["possible_reflected_xss"], bool)
