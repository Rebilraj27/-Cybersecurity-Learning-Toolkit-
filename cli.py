import argparse
import sys
from rich.console import Console
from toolkit import port_scanner, password_strength, hash_cracker, encrypter, web_vuln_scanner

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Cybersecurity Learning Toolkit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # portscan
    p = sub.add_parser("portscan")
    p.add_argument("host")
    p.add_argument("--ports", default="1-1024")
    p.add_argument("--workers", type=int, default=100)

    # passwd
    p = sub.add_parser("passwd")
    p.add_argument("password")

    # crack
    p = sub.add_parser("crack")
    p.add_argument("hash")
    p.add_argument("wordlist")
    p.add_argument("--algo", default="md5", choices=["md5", "sha1", "sha256", "sha512"])

    # encrypt / decrypt
    p = sub.add_parser("encrypt")
    p.add_argument("text")
    p.add_argument("password")

    p = sub.add_parser("decrypt")
    p.add_argument("token")
    p.add_argument("password")

    # webs scan
    p = sub.add_parser("webscan")
    p.add_argument("url")

    args = parser.parse_args()

    if args.cmd == "portscan":
        if "-" in args.ports:
            a, b = map(int, args.ports.split("-"))
            ports = list(range(a, b + 1))
        else:
            ports = [int(x) for x in args.ports.split(",")]
        port_scanner.scan(args.host, ports, args.workers)

    elif args.cmd == "passwd":
        result = password_strength.analyze(args.password)
        console.print(f"[bold]Strength:[/] {result['strength']}")
        console.print(f"[bold]Entropy:[/] {result['entropy_bits']} bits")
        for f in result["feedback"]:
            console.print(f"  [yellow]• {f}[/]")

    elif args.cmd == "crack":
        r = hash_cracker.crack(args.hash, args.wordlist, args.algo)
        if r["found"]:
            console.print(f"[green]✔ Cracked:[/] {r['password']} ({r['attempts']} tries)")
        else:
            console.print("[red]✘ Not found in wordlist[/]")

    elif args.cmd == "encrypt":
        console.print(encrypter.encrypt(args.text, args.password))

    elif args.cmd == "decrypt":
        try:
            console.print(encrypter.decrypt(args.token, args.password))
        except Exception:
            console.print("[red]Decryption failed[/]")

    elif args.cmd == "webscan":
        import json
        console.print(json.dumps(web_vuln_scanner.scan(args.url), indent=2))

if __name__ == "__main__":
    main()
