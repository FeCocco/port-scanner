#!/usr/bin/env python3

#portscan.py — simple educational port scanner 

from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import argparse
import csv
import json
import sys
from datetime import datetime

RED_BOLD = "\033[1;31m"
RESET = "\033[0m"

DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389]

def parse_ports(ports_str):
    """
    Accepts:
    - "22,80,443"
    - "1-1024"
    - combination "22,80,1000-1010"
    Returns a sorted list of unique ports.
    """
    ports = set()
    if not ports_str:
        return DEFAULT_PORTS[:]
    parts = ports_str.split(",")
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if "-" in p:
            try:
                a, b = p.split("-", 1)
                a = int(a); b = int(b)
                if a > b:
                    a, b = b, a
                # clamp to valid port range
                a = max(1, a)
                b = min(65535, b)
                if a <= b:
                    ports.update(range(a, b + 1))
            except ValueError:
                continue
        else:
            try:
                num = int(p)
                if 1 <= num <= 65535:
                    ports.add(num)
            except ValueError:
                continue
    return sorted(ports)

def scan_port(host_ip, port, timeout):
    """
    TCP connection. Return a dict with results.
    """
    try:
        with socket.create_connection((host_ip, port), timeout=timeout):
            return {"port": port, "open": True, "error": None}
    except socket.timeout:
        return {"port": port, "open": False, "error": "timeout"}
    except ConnectionRefusedError:
        return {"port": port, "open": False, "error": "refused"}
    except OSError as e:
        return {"port": port, "open": False, "error": str(e)}
    except Exception as e:
        return {"port": port, "open": False, "error": f"unexpected:{e}"}

def save_json(results, path):
    payload = {
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "results": results
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def save_csv(results, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["port", "open", "error"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

def main():
    parser = argparse.ArgumentParser(description="Educational port scanner (use only on authorized targets).")
    parser.add_argument("-t", "--target", required=True, help="Target hostname or IP")
    parser.add_argument("-p", "--ports", default="", help="Ports (e.g. '22,80,443' or '1-1024' or combination)")
    parser.add_argument("-T", "--timeout", type=float, default=0.5, help="Connection timeout in seconds (default: 0.5)")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Number of worker threads (default: 50)")
    parser.add_argument("-o", "--out", default="", help="Output prefix (generates <prefix>.json and <prefix>.csv)")
    parser.add_argument("--no-disclaimer", action="store_true", help="Skip disclaimer message")
    args = parser.parse_args()

    disclaimer = (
        "DISCLAIMER — READ THIS\n"
		"This script is for educational use only. Do not run it against systems you don't own or don't have written permission to test.\n"
		"I know you're tempted — 'just one quick scan' is how trouble starts. If you use it without authorization, it's on you, not me.\n"
    )
    if not args.no_disclaimer:
    	print(RED_BOLD + disclaimer + RESET)
    
    target = args.target
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Unable to resolve host: {target}", file=sys.stderr)
        sys.exit(1)

    ports = parse_ports(args.ports)
    if not ports:
        print("[!] No valid ports specified.", file=sys.stderr)
        sys.exit(1)

    print(f"[i] Scanning {target} ({ip}) — {len(ports)} ports — timeout {args.timeout}s — workers {args.workers}")
    results = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_port = {executor.submit(scan_port, ip, port, args.timeout): port for port in ports}
        try:
            for fut in as_completed(future_to_port):
                res = fut.result()
                results.append(res)
                if res["open"]:
                    print(f"[+] Port {res['port']} -> OPEN")
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user. Shutting down...")
            executor.shutdown(wait=False)
            sys.exit(1)

    results = sorted(results, key=lambda x: x["port"])
    if args.out:
        json_path = f"{args.out}.json"
        csv_path = f"{args.out}.csv"
        save_json(results, json_path)
        save_csv(results, csv_path)
        print(f"[i] Results saved: {json_path}, {csv_path}")

    open_ports = [r["port"] for r in results if r["open"]]
    print(f"[i] Scan finished. Open ports: {open_ports if open_ports else 'none found.'}")

if __name__ == "__main__":
    main()
