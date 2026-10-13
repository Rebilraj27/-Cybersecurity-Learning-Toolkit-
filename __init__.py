"""
Cyber Toolkit
=============
A Python-based cybersecurity learning toolkit.

Created by: Rebilraj
License:    MIT
Purpose:    Educational & ethical cybersecurity learning only.

Modules
-------
- port_scanner       : Multi-threaded TCP port scanner with banner grabbing
- password_strength  : Password entropy & strength analyzer
- hash_cracker       : Dictionary-based hash cracker (MD5/SHA1/SHA256/SHA512)
- encrypter          : AES-GCM encryption with PBKDF2 key derivation
- web_vuln_scanner   : Basic web vulnerability scanner
- network_sniffer    : Packet sniffer & analyzer (Scapy-based)

⚠️  Legal Notice
----------------
This package is for EDUCATIONAL purposes only. Only use it on systems
you own or have explicit written authorization to test. Unauthorized
access to computer systems is illegal.
"""

__version__ = "1.0.0"
__author__ = "Rebilraj"
__license__ = "MIT"
__all__ = [
    "port_scanner",
    "password_strength",
    "hash_cracker",
    "encrypter",
    "web_vuln_scanner",
    "network_sniffer",
]


def banner() -> str:
    """Return the Cyber Toolkit ASCII banner as a string."""
    return r"""
╔═══════════════════════════════════════════════════════════════╗
║   ██████╗██╗   ██╗██████╗ ███████╗██████╗                     ║
║  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗                    ║
║  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝                    ║
║  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗                    ║
║  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║                    ║
║   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝                    ║
║                                                               ║
║              ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
║              ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
║                 ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
║                 ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
║                 ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
║                 ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
║                                                               ║
║                    Created by: Rebilraj                       ║
║              Ethical Hacking Learning Toolkit                 ║
╚═══════════════════════════════════════════════════════════════╝
"""
