"""
Tests for toolkit.network_sniffer
Uses pre-built Scapy packets — no live capture required (no root needed).
"""

import pytest

from toolkit import network_sniffer

scapy = pytest.importorskip("scapy.all")


class TestGetProtocol:

    def test_detects_http(self, scapy_packets):
        assert network_sniffer.get_protocol(scapy_packets["tcp_syn"]) == "HTTP"

    def test_detects_https(self, scapy_packets):
        assert network_sniffer.get_protocol(scapy_packets["tcp_https"]) == "HTTPS"

    def test_detects_dns(self, scapy_packets):
        assert network_sniffer.get_protocol(scapy_packets["udp_dns"]) == "DNS"

    def test_detects_icmp(self, scapy_packets):
        assert network_sniffer.get_protocol(scapy_packets["icmp"]) == "ICMP"

    def test_detects_arp(self, scapy_packets):
        assert network_sniffer.get_protocol(scapy_packets["arp"]) == "ARP"

    def test_unknown_tcp_port(self):
        pkt = scapy.IP() / scapy.TCP(sport=1111, dport=9999)
        assert network_sniffer.get_protocol(pkt) == "TCP"

    def test_unknown_udp_port(self):
        pkt = scapy.IP() / scapy.UDP(sport=1111, dport=9999)
        assert network_sniffer.get_protocol(pkt) == "UDP"


class TestExtractInfo:

    def test_extracts_ip_and_ports(self, scapy_packets):
        info = network_sniffer.extract_info(scapy_packets["tcp_syn"])
        assert info["src"] == "10.0.0.1"
        assert info["dst"] == "10.0.0.2"
        assert info["sport"] == 12345
        assert info["dport"] == 80
        assert info["protocol"] == "HTTP"

    def test_extracts_dns_query(self, scapy_packets):
        info = network_sniffer.extract_info(scapy_packets["udp_dns"])
        assert info["protocol"] == "DNS"
        assert "example.com" in info.get("dns_query", "")

    def test_extracts_arp_addresses(self, scapy_packets):
        info = network_sniffer.extract_info(scapy_packets["arp"])
        assert info["src"] == "10.0.0.1"
        assert info["protocol"] == "ARP"

    def test_size_is_int(self, scapy_packets):
        info = network_sniffer.extract_info(scapy_packets["tcp_syn"])
        assert isinstance(info["size"], int) and info["size"] > 0

    def test_payload_preview(self, scapy_packets):
        info = network_sniffer.extract_info(scapy_packets["http_payload"])
        assert "payload_preview" in info
        assert "GET /" in info["payload_preview"]


class TestSnifferStats:

    def test_init_defaults(self):
        s = network_sniffer.Sniffer()
        assert s.packets == []
        assert s.max_packets == 0
        assert s.show_payload is False

    def test_handle_packet_updates_counters(self, scapy_packets):
        s = network_sniffer.Sniffer()
        s._handle_packet(scapy_packets["tcp_syn"])
        s._handle_packet(scapy_packets["udp_dns"])
        assert len(s.packets) == 2
        assert s.protocol_counts["HTTP"] == 1
        assert s.protocol_counts["DNS"] == 1

    def test_max_packets_stops(self, scapy_packets):
        s = network_sniffer.Sniffer(max_packets=1)
        s.running = True
        s._handle_packet(scapy_packets["tcp_syn"])
        assert s.running is False

    def test_port_counts(self, scapy_packets):
        s = network_sniffer.Sniffer()
        s._handle_packet(scapy_packets["tcp_syn"])
        assert s.port_counts[80] == 1


class TestInterfaces:

    def test_list_interfaces_returns_list(self):
        assert isinstance(network_sniffer.list_interfaces(), list)

    def test_scapy_available(self):
        assert network_sniffer.SCAPY_AVAILABLE is True


class TestPcapAnalysis:

    def test_analyze_pcap(self, tmp_path, scapy_packets):
        pcap_file = tmp_path / "test.pcap"
        scapy.wrpcap(str(pcap_file), [
            scapy_packets["tcp_syn"],
            scapy_packets["udp_dns"],
        ])
        result = network_sniffer.analyze_pcap(str(pcap_file))
        assert result["total_packets"] == 2
        assert result["protocols"]["HTTP"] == 1
        assert result["protocols"]["DNS"] == 1

    def test_analyze_nonexistent_pcap(self):
        with pytest.raises(Exception):
            network_sniffer.analyze_pcap("/no/such/file.pcap")
