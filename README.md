<!-- ============================================= -->
<!--                 BANNER SECTION                -->
<!-- ============================================= -->

<div align="center">

```
    ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
   ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
   ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
   ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
   ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
    ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝

    ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║   
       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║   
       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║   
       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   
```

### 🛡️ A Modular Cybersecurity Learning Toolkit

**Built for ethical hackers, students, and security researchers.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue?style=for-the-badge)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)]()
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=for-the-badge)]()

</div>

---

## ⚠️ LEGAL DISCLAIMER

> **🚨 READ BEFORE USE 🚨**
>
> This toolkit is designed **strictly for educational purposes** and **authorized security testing**.
>
> ✅ **Allowed:**
> - Your own systems and lab environments
> - CTF competitions
> - Authorized penetration tests (with **written permission**)
> - Security research in isolated VMs
>
> ❌ **Prohibited:**
> - Unauthorized access to any system
> - Attacking networks without explicit consent
> - Any illegal activity
>
> **Unauthorized use is a criminal offense** under laws including CFAA (US), IT Act 2000 (India), Computer Misuse Act (UK), and GDPR (EU).
>
> **The authors assume NO liability for misuse.** You are solely responsible for your actions.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Requirements](#-requirements)
- [Installation](#-installation)
  - [Method 1: Quick Install (pip)](#method-1-quick-install-pip)
  - [Method 2: Development Setup](#method-2-development-setup)
  - [Method 3: Docker](#method-3-docker)
  - [Method 4: Virtual Environment (Recommended)](#method-4-virtual-environment-recommended)
- [Usage](#-usage)
- [Modules](#-modules)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Practice Labs](#-practice-labs)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 Overview

**Cyber Toolkit** is a Python-based, modular cybersecurity toolkit for **learning, testing, and research**. It bundles essential security utilities into a single, clean CLI — no more juggling 10 different tools.

Built with a focus on:
- 🎯 **Simplicity** – One command, one task
- 🔧 **Modularity** – Use only what you need
- 📚 **Education** – Well-commented, readable code
- 🎨 **UX** – Beautiful terminal output via `rich`

---

## ✨ Features

| Module | Description | Status |
|--------|-------------|--------|
| 🔍 **Port Scanner** | Multi-threaded TCP scanner with banner grabbing | ✅ Stable |
| 🔐 **Password Analyzer** | Entropy-based password strength analysis | ✅ Stable |
| 🧨 **Hash Cracker** | Dictionary attack on MD5/SHA1/SHA256/SHA512 | ✅ Stable |
| 🔒 **AES Encrypter** | AES-256-GCM encryption with PBKDF2 key derivation | ✅ Stable |
| 🌐 **Web Scanner** | Header analysis + reflected XSS detection | ✅ Stable |
| 📡 **Network Sniffer** | Packet capture and analysis (Scapy) | 🚧 Beta |
| 🕵️ **Subdomain Finder** | DNS enumeration and subdomain discovery | 🚧 Beta |

---

## 🖼️ Screenshots

> Terminal output examples (rendered with `rich`)

**Port Scan:**
```
╭──────────────── Open Ports on 192.168.56.10 ────────────────╮
│ Port   Service       Banner                                 │
│ 22     SSH           SSH-2.0-OpenSSH_8.2p1 Ubuntu          │
│ 80     HTTP          Apache/2.4.41 (Ubuntu)                │
│ 3306   MySQL         -                                      │
╰─────────────────────────────────────────────────────────────╯
```

**Password Analysis:**
```
Strength: Strong
Entropy:  89.4 bits
  • Add symbols
```

---

## 📋 Requirements

### Minimum
- **Python:** 3.9 or higher
- **OS:** Linux, macOS, or Windows 10+
- **RAM:** 512 MB
- **Disk:** 50 MB

### Optional (for full functionality)
- `nmap` – for extended port scanning
- `libpcap` – for packet sniffing (Linux/macOS)
- `Npcap` – for packet sniffing (Windows)

### Verify Python version:
```bash
python3 --version   # Should print 3.9+
```

---

## 🚀 Installation

### Method 1: Quick Install (pip)

**For users who just want to run it:**

```bash
# 1. Clone the repo
git clone https://github.com/your-username/cyber-toolkit.git
cd cyber-toolkit

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python cli.py --help
```

---

### Method 2: Development Setup

**For contributors and tinkerers:**

```bash
# 1. Clone
git clone https://github.com/your-username/cyber-toolkit.git
cd cyber-toolkit

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate          # Linux / macOS
# OR
venv\Scripts\activate             # Windows

# 3. Upgrade pip and install
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .                  # Editable install

# 4. Run tests
pytest tests/ -v

# 5. Launch
python cli.py --help
```

---

### Method 3: Docker

**Isolated, portable, safe:**

**`Dockerfile`** (already in repo):
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["python", "cli.py"]
```

**Build & Run:**
```bash
# Build image
docker build -t cyber-toolkit .

# Run a scan (mount wordlists as needed)
docker run --rm -it cyber-toolkit portscan 192.168.56.10

# Persist wordlists
docker run --rm -it -v $(pwd)/wordlists:/app/wordlists cyber-toolkit crack <hash> /app/wordlists/rockyou.txt
```

> **Note:** For network scanning from Docker, use `--network=host` (Linux) or map ports appropriately.

---

### Method 4: Virtual Environment (Recommended)

**Best isolation, avoids system conflicts:**

```bash
# Clone
git clone https://github.com/your-username/cyber-toolkit.git
cd cyber-toolkit

# Create + activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install with upgrade
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Verify installation
python -c "import scapy, requests, rich, cryptography; print('✅ All modules OK')"
```

**Deactivate when done:**
```bash
deactivate
```

---

### 🐧 Platform-Specific Notes

#### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv libpcap-dev nmap
pip install -r requirements.txt
```

#### macOS
```bash
# Install Homebrew if missing
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python@3.11 nmap
pip3 install -r requirements.txt
```

#### Windows (PowerShell)
```powershell
# Install Python from python.org, then:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# For Scapy (packet sniffing), install Npcap from https://npcap.com
```

> **Windows users:** Run terminal **as Administrator** for raw socket operations.

---

## 🎯 Usage

### Basic CLI Syntax
```bash
python cli.py <command> [options]
```

### Command Reference

#### 🔍 Port Scanner
```bash
# Scan common ports
python cli.py portscan 192.168.56.10

# Scan a port range
python cli.py portscan 192.168.56.10 --ports 1-1024

# Scan specific ports
python cli.py portscan 192.168.56.10 --ports 22,80,443,3306

# Adjust speed
python cli.py portscan 192.168.56.10 --ports 1-65535 --workers 500
```

#### 🔐 Password Analyzer
```bash
python cli.py passwd "MyS3cur3P@ss!"
```
Output:
```
Strength: Very Strong
Entropy:  104.2 bits
```

#### 🧨 Hash Cracker
```bash
python cli.py crack 5f4dcc3b5aa765d61d8327deb882cf99 wordlists/rockyou.txt --algo md5
```

#### 🔒 AES Encryption
```bash
# Encrypt
python cli.py encrypt "top secret" "mypassword"

# Decrypt
python cli.py decrypt "<base64_blob>" "mypassword"
```

#### 🌐 Web Scanner
```bash
python cli.py webscan "http://localhost:8080/?q=test"
```

---

## 🧩 Modules

| File | Purpose |
|------|---------|
| `toolkit/port_scanner.py` | Async TCP port scanner + banner grab |
| `toolkit/password_strength.py` | Entropy calculator and rule-based scoring |
| `toolkit/hash_cracker.py` | Dict attack for common hash algorithms |
| `toolkit/encrypter.py` | AES-256-GCM with PBKDF2 (200k iterations) |
| `toolkit/web_vuln_scanner.py` | Header check + reflected XSS probing |
| `toolkit/network_sniffer.py` | Packet capture (Scapy) |

Each module can be imported independently:
```python
from toolkit import port_scanner
port_scanner.scan("192.168.56.10", [22, 80, 443])
```

---

## ⚙️ Configuration

Create a `config.yaml` (optional):
```yaml
scan:
  default_timeout: 1.0
  max_workers: 100
  banner_grab: true

hash:
  wordlist_path: "./wordlists/rockyou.txt"
  default_algo: "md5"

web:
  user_agent: "CyberToolkit/1.0"
  timeout: 5
```

Load it in your scripts:
```python
import yaml
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)
```

---

## 📂 Project Structure

```
cyber-toolkit/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── Dockerfile
├── config.yaml
├── cli.py
├── toolkit/
│   ├── __init__.py
│   ├── port_scanner.py
│   ├── hash_cracker.py
│   ├── password_strength.py
│   ├── encrypter.py
│   ├── web_vuln_scanner.py
│   └── network_sniffer.py
├── wordlists/
│   └── README.md
├── tests/
│   ├── test_port_scanner.py
│   ├── test_password_strength.py
│   └── test_encrypter.py
└── docs/
    ├── INSTALL.md
    └── USAGE.md
```

---

## 🧪 Practice Labs

**Practice legally in these environments:**

| Platform | Type | Cost |
|----------|------|------|
| [TryHackMe](https://tryhackme.com) | Guided rooms | Free + Paid |
| [HackTheBox](https://hackthebox.com) | CTF challenges | Free + Paid |
| [PortSwigger Academy](https://portswigger.net/web-security) | Web security | Free |
| [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) | Vulnerable web app | Free |
| [DVWA](https://github.com/digininja/DVWA) | Vulnerable PHP app | Free |
| [Metasploitable2](https://sourceforge.net/projects/metasploitable/) | Vulnerable VM | Free |

> 💡 Always run these inside **VirtualBox** or **VMware** with a **host-only network** to isolate them from your real LAN.

---

## 🐛 Troubleshooting

### `ModuleNotFoundError: No module named 'scapy'`
```bash
pip install scapy --upgrade
```

### `Permission denied` on Linux (port scanning)
```bash
sudo setcap cap_net_raw,cap_net_admin=eip $(readlink -f $(which python3))
```

### Windows: `[WinError 10013]` on sniffing
- Install **Npcap** from https://npcap.com
- Run terminal as **Administrator**

### Slow port scans
- Increase workers: `--workers 500`
- Reduce timeout in `port_scanner.py`

### `cryptography` build fails on macOS
```bash
brew install openssl rust
export LDFLAGS="-L$(brew --prefix openssl)/lib"
pip install cryptography
```

---

## 🤝 Contributing

We love contributions! Here's how:

1. **Fork** the repo
2. **Branch:** `git checkout -b feature/amazing-module`
3. **Commit:** `git commit -m "Add amazing module"`
4. **Push:** `git push origin feature/amazing-module`
5. **Open a Pull Request**

### Guidelines
- ✅ Write tests for new modules
- ✅ Follow PEP 8 style
- ✅ Update README if you add a new command
- ✅ Never include malicious payloads

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

```
MIT License

Copyright (c) 2025 Cyber Toolkit Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- Inspired by tools like **Nmap**, **Hydra**, **Burp Suite**, and **hashcat**
- Thanks to the **Python security community**
- Built with [Rich](https://github.com/Textualize/rich), [Scapy](https://scapy.net), [Cryptography](https://cryptography.io)

---

## ⭐ Star History

If this project helped you learn, **please star it!** ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/cyber-toolkit&type=Date)](https://star-history.com/#your-username/cyber-toolkit)

---

<div align="center">

**Made with ❤️ for the security community**

*"With great power comes great responsibility."* — Uncle Ben

**[⬆ Back to Top](#-complete-readmemd-for-cyber-toolkit)**

</div>
