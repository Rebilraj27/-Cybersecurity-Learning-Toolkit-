"""
network_sniffer.py
==================
Packet sniffer and analyzer using Scapy.

⚠️  WARNING
-----------
Sniffing network traffic on networks you do NOT own or have
explicit written permission to monitor is ILLEGAL in most
jurisdictions. Use only on:
  - Your own home lab
  - Authorized penetration tests
  - CTF environments
  - Your own machine traffic

Created by: Rebilraj
License:    MIT
"""

from __future__ import annotations

import argparse
import time
from collections import Counter, defaultdict
from datetime import datetime
from typing import Optional

try:
    from scapy.all import (
        sniff,
        conf,
        IP,
        IPv6,
        TCP,
        UDP,
        ICMP,
        ARP,
        DNS,
        DNSQR,
        Raw,
        get_if_list,
    )
    from scapy.error import Scapy_Exception
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

console = Console()


# ─────────────────────────────────────────────────────────────
#  Packet Analysis Helpers
# ─────────────────────────────────────────────────────────────

def get_protocol(pkt) -> str:
    """Return a human-readable protocol name for a packet."""
    if pkt.haslayer(ARP):
        return "ARP"
    if pkt.haslayer(ICMP):
        return "ICMP"
    if pkt.haslayer(DNS):
        return "DNS"
    if pkt.haslayer(TCP):
        # Identify common TCP services by port
        tcp = pkt[TCP]
        for port, name in ((80, "HTTP"), (443, "HTTPS"), (22, "SSH"),
                           (21, "FTP"), (25, "SMTP"), (3306, "MySQL"),
                           (5432, "PostgreSQL"), (3389, "RDP")):
            if port in (tcp.sport, tcp.dport):
                return name
        return "TCP"
    if pkt.haslayer(UDP):
        return "UDP"
    if pkt.haslayer(IP) or pkt.haslayer(IPv6):
        return "IP"
    return "OTHER"


def extract_info(pkt) -> dict:
    """Extract relevant fields from a packet into a dict."""
    info = {
        "src": "?",
        "dst": "?",
        "sport": "-",
        "dport": "-",
        "protocol": get_protocol(pkt),
        "size": len(pkt),
        "summary": pkt.summary(),
    }

    if pkt.haslayer(IP):
        info["src"] = pkt[IP].src
        info["dst"] = pkt[IP].dst
    elif pkt.haslayer(IPv6):
        info["src"] = pkt[IPv6].src
        info["dst"] = pkt[IPv6].dst
    elif pkt.haslayer(ARP):
        info["src"] = pkt[ARP].psrc
        info["dst"] = pkt[ARP].pdst

    if pkt.haslayer(TCP):
        info["sport"] = pkt[TCP].sport
        info["dport"] = pkt[TCP].dport
    elif pkt.haslayer(UDP):
        info["sport"] = pkt[UDP].sport
        info["dport"] = pkt[UDP].dport

    if pkt.haslayer(DNSQR):
        try:
            info["dns_query"] = pkt[DNSQR].qname.decode(errors="ignore")
        except Exception:
            pass

    if pkt.haslayer(Raw):
        try:
            payload = pkt[Raw].load[:120]
            info["payload_preview"] = payload.decode(errors="ignore").strip()
        except Exception:
            pass

    return info


# ─────────────────────────────────────────────────────────────
#  Live Sniffer
# ─────────────────────────────────────────────────────────────

class Sniffer:
    """Live network packet sniffer with statistics."""

    def __init__(
        self,
        iface: Optional[str] = None,
        bpf_filter: str = "",
        max_packets: int = 0,
        show_payload: bool = False,
    ):
        self.iface = iface
        self.bpf_filter = bpf_filter
        self.max_packets = max_packets
        self.show_payload = show_payload

        self.packets = []
        self.protocol_counts = Counter()
        self.src_ip_counts = Counter()
        self.dst_ip_counts = Counter()
        self.port_counts = Counter()
        self.start_time = None
        self.running = False

    # ── packet callback ─────────────────────────────────────
    def _handle_packet(self, pkt):
        self.packets.append(pkt)
        info = extract_info(pkt)

        self.protocol_counts[info["protocol"]] += 1
        if info["src"] != "?":
            self.src_ip_counts[info["src"]] += 1
        if info["dst"] != "?":
            self.dst_ip_counts[info["dst"]] += 1
        if info["dport"] != "-":
            self.port_counts[info["dport"]] += 1

        # Live print
        ts = datetime.now().strftime("%H:%M:%S")
        line = (
            f"[dim]{ts}[/] "
            f"[cyan]{info['protocol']:>5}[/] "
            f"[green]{info['src']}:{info['sport']}[/] → "
            f"[yellow]{info['dst']}:{info['dport']}[/] "
            f"[white]({info['size']}B)[/]"
        )
        console.print(line)

        if self.show_payload and "payload_preview" in info:
            console.print(f"  [magenta]↳ {info['payload_preview']}[/]")
        if "dns_query" in info:
            console.print(f"  [blue]↳ DNS Query: {info['dns_query']}[/]")

        if self.max_packets and len(self.packets) >= self.max_packets:
            self.running = False

    # ── start capture ───────────────────────────────────────
    def start(self):
        if not SCAPY_AVAILABLE:
            console.print(
                "[bold red]✘ Scapy not installed.[/]\n"
                "Install with: [cyan]pip install scapy[/]"
            )
            return

        console.print(Panel.fit(
            f"[bold cyan]Cyber Toolkit — Network Sniffer[/]\n"
            f"[white]Interface :[/] [yellow]{self.iface or 'default'}[/]\n"
            f"[white]BPF Filter:[/] [yellow]{self.bpf_filter or 'none'}[/]\n"
            f"[white]Max Pkts  :[/] [yellow]{self.max_packets or 'unlimited'}[/]\n"
            f"[dim]Press Ctrl+C to stop[/]",
            title="[bold green]▶ Capture Started[/]",
            border_style="green",
        ))

        self.start_time = time.time()
        self.running = True

        try:
            sniff(
                iface=self.iface,
                filter=self.bpf_filter,
                prn=self._handle_packet,
                store=False,
                stop_filter=lambda _: not self.running,
            )
        except KeyboardInterrupt:
            console.print("\n[yellow]⏹  Capture stopped by user[/]")
        except Scapy_Exception as e:
            console.print(f"[bold red]✘ Scapy error:[/] {e}")
            console.print(
                "[dim]Tip: On Linux/macOS you may need [cyan]sudo[/]. "
                "On Windows install [cyan]Npcap[/].[/]"
            )
            return
        except PermissionError:
            console.print(
                "[bold red]✘ Permission denied.[/] "
                "Run as [cyan]sudo[/] (Linux) or Administrator (Windows)."
            )
            return

        self.print_summary()

    # ── summary ─────────────────────────────────────────────
    def print_summary(self):
        duration = time.time() - self.start_time if self.start_time else 0
        total = len(self.packets)

        console.print()
        console.print(Panel.fit(
            f"[white]Duration :[/] [cyan]{duration:.2f}s[/]\n"
            f"[white]Packets  :[/] [cyan]{total}[/]\n"
            f"[white]Rate     :[/] [cyan]{total / duration:.1f} pkt/s[/]"
            if duration > 0 else f"[white]Packets:[/] [cyan]{total}[/]",
            title="[bold green]📊 Capture Summary[/]",
            border_style="green",
        ))

        # Protocol breakdown
        if self.protocol_counts:
            t = Table(title="Protocol Breakdown", header_style="bold magenta")
            t.add_column("Protocol", style="cyan")
            t.add_column("Count", justify="right", style="green")
            t.add_column("%", justify="right", style="yellow")
            for proto, count in self.protocol_counts.most_common():
                pct = (count / total) * 100 if total else 0
                t.add_row(proto, str(count), f"{pct:.1f}%")
            console.print(t)

        # Top talkers
        if self.src_ip_counts:
            t = Table(title="Top Source IPs", header_style="bold magenta")
            t.add_column("Source IP", style="cyan")
            t.add_column("Packets", justify="right", style="green")
            for ip, count in self.src_ip_counts.most_common(5):
                t.add_row(ip, str(count))
            console.print(t)

        if self.dst_ip_counts:
            t = Table(title="Top Destination IPs", header_style="bold magenta")
            t.add_column("Dest IP", style="cyan")
            t.add_column("Packets", justify="right", style="green")
            for ip, count in self.dst_ip_counts.most_common(5):
                t.add_row(ip, str(count))
            console.print(t)

        if self.port_counts:
            t = Table(title="Top Destination Ports", header_style="bold magenta")
            t.add_column("Port", style="cyan")
            t.add_column("Packets", justify="right", style="green")
            for port, count in self.port_counts.most_common(5):
                t.add_row(str(port), str(count))
            console.print(t)


# ─────────────────────────────────────────────────────────────
#  Offline PCAP Analysis
# ─────────────────────────────────────────────────────────────

def analyze_pcap(path: str) -> dict:
    """Analyze a saved .pcap file and return statistics."""
    if not SCAPY_AVAILABLE:
        raise RuntimeError("Scapy is required. Install with: pip install scapy")

    from scapy.all import rdpcap

    packets = rdpcap(path)
    proto_counts = Counter()
    src_counts = Counter()
    dst_counts = Counter()

    for pkt in packets:
        info = extract_info(pkt)
        proto_counts[info["protocol"]] += 1
        if info["src"] != "?":
            src_counts[info["src"]] += 1
        if info["dst"] != "?":
            dst_counts[info["dst"]] += 1

    return {
        "file": path,
        "total_packets": len(packets),
        "protocols": dict(proto_counts),
        "top_sources": src_counts.most_common(10),
        "top_destinations": dst_counts.most_common(10),
    }


# ─────────────────────────────────────────────────────────────
#  Interface Listing
# ─────────────────────────────────────────────────────────────

def list_interfaces() -> list[str]:
    """Return available network interfaces."""
    if not SCAPY_AVAILABLE:
        return []
    try:
        return get_if_list()
    except Exception:
        return []


def show_interfaces():
    """Pretty-print available network interfaces."""
    ifaces = list_interfaces()
    if not ifaces:
        console.print("[yellow]No interfaces found (is Scapy installed?)[/]")
        return

    t = Table(title="Available Network Interfaces", header_style="bold cyan")
    t.add_column("#", style="dim")
    t.add_column("Interface", style="green")
    for i, iface in enumerate(ifaces, 1):
        t.add_row(str(i), iface)
    console.print(t)


# ─────────────────────────────────────────────────────────────
#  CLI Entry (used when run directly)
# ─────────────────────────────────────────────────────────────

def _cli():
    parser = argparse.ArgumentParser(
        description="Cyber Toolkit — Network Sniffer (by Rebilraj)"
    )
    parser.add_argument("-i", "--iface", help="Network interface to sniff on")
    parser.add_argument("-f", "--filter", default="",
                        help="BPF filter (e.g., 'tcp port 80')")
    parser.add_argument("-c", "--count", type=int, default=0,
                        help="Stop after N packets (0 = unlimited)")
    parser.add_argument("-p", "--payload", action="store_true",
                        help="Show payload preview")
    parser.add_argument("-l", "--list", action="store_true",
                        help="List available interfaces")
    parser.add_argument("--pcap", help="Analyze a .pcap file instead of live capture")

    args = parser.parse_args()

    if args.list:
        show_interfaces()
        return

    if args.pcap:
        import json
        console.print(json.dumps(analyze_pcap(args.pcap), indent=2))
        return

    sniffer = Sniffer(
        iface=args.iface,
        bpf_filter=args.filter,
        max_packets=args.count,
        show_payload=args.payload,
    )
    sniffer.start()


if __name__ == "__main__":
    _cli()
