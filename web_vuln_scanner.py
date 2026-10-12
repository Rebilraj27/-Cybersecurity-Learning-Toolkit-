import requests
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

XSS_PAYLOAD = "<script>alert(1)</script>"
SQLI_PAYLOAD = "' OR '1'='1"

def check_headers(url: str) -> list[str]:
    issues = []
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException as e:
        return [f"Request failed: {e}"]

    required = {
        "Content-Security-Policy": "Missing CSP header",
        "X-Frame-Options": "Missing X-Frame-Options (clickjacking risk)",
        "Strict-Transport-Security": "Missing HSTS",
        "X-Content-Type-Options": "Missing X-Content-Type-Options",
    }
    for header, msg in required.items():
        if header not in r.headers:
            issues.append(msg)
    return issues

def test_reflected_xss(url: str) -> bool:
    """Only test on YOUR OWN lab apps."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if not params:
        return False
    for key in params:
        test_params = {**params, key: [XSS_PAYLOAD]}
        test_url = parsed._replace(query=urlencode(test_params, doseq=True)).geturl()
        try:
            r = requests.get(test_url, timeout=5)
            if XSS_PAYLOAD in r.text:
                return True
        except requests.RequestException:
            pass
    return False

def scan(url: str) -> dict:
    return {
        "url": url,
        "header_issues": check_headers(url),
        "possible_reflected_xss": test_reflected_xss(url),
    }
