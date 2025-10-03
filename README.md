# portscan.py

A simple TCP port scanner for when you need to know what's open (and you have permission to ask).

## DISCLAIMER – READ THIS

**This is for educational use and authorized testing only.**

Look, I know you're tempted. "Just one quick scan" is how problems start. This tool is for:
- Your own systems
- Lab environments
- Pentesting gigs where you have written permission
- CTF competitions

If you use this on systems you don't own or don't have explicit authorization for, that's on you. I'm not your lawyer, but unauthorized port scanning can land you in hot water legally. Don't be that person.

## Features

- Fast concurrent scanning (50 threads by default, bump it up if you're feeling spicy)
- Flexible port specs: single ports, ranges, or mix them up
- Multiple output formats because sometimes you need a CSV for that report
- Configurable timeout – go fast or go accurate, your choice
- Detailed error reporting so you know why things failed
- Automatic hostname resolution because who remembers IPs anyway

## Requirements

- Python 3.6+
- That's it. No pip install hell here.

## Installation

```bash
git clone https://github.com/your-username/portscan.git
cd portscan
chmod +x portscan.py  # Linux/Mac users
```

Done. See? Simple.

## Usage

### Basic Syntax

```bash
python3 portscan.py -t <target> [options]
```

### Examples

**Scan default ports (the usual suspects):**
```bash
python3 portscan.py -t example.com
```

**Specific ports:**
```bash
python3 portscan.py -t 192.168.1.1 -p 22,80,443,8080
```

**Port range (classic 1-1024):**
```bash
python3 portscan.py -t example.com -p 1-1024
```

**Get creative with it:**
```bash
python3 portscan.py -t example.com -p 22,80,443,8000-9000
```

**Speed demon mode (more workers, longer timeout):**
```bash
python3 portscan.py -t example.com -p 1-65535 -T 1.0 -w 100
```

**Save results (for that professional touch):**
```bash
python3 portscan.py -t example.com -p 1-1000 -o scan_results
# Creates scan_results.json and scan_results.csv
```

**Skip the disclaimer (automation friendly):**
```bash
python3 portscan.py -t example.com --no-disclaimer
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `-t, --target` | Target hostname or IP (required) | - |
| `-p, --ports` | Ports to scan | 21,22,23,25,53,80,110,143,443,445,3306,3389 |
| `-T, --timeout` | Connection timeout in seconds | 0.5 |
| `-w, --workers` | Number of concurrent threads | 50 |
| `-o, --out` | Output file prefix | - |
| `--no-disclaimer` | Skip the disclaimer | False |

## Output Format

### Terminal
```
[i] Scanning example.com (93.184.216.34) – 12 ports – timeout 0.5s – workers 50
[+] Port 80 -> OPEN
[+] Port 443 -> OPEN
[i] Scan finished. Open ports: [80, 443]
```

### JSON (`scan_results.json`)
```json
{
  "scanned_at": "2025-10-02T14:30:00.123456Z",
  "results": [
    {"port": 80, "open": true, "error": null},
    {"port": 443, "open": true, "error": null},
    {"port": 22, "open": false, "error": "refused"}
  ]
}
```

### CSV (`scan_results.csv`)
```csv
port,open,error
80,True,
443,True,
22,False,refused
```

## How It Works

Pretty straightforward:

1. Resolves your target to an IP
2. Parses whatever port mess you threw at it
3. Fires up a thread pool and starts knocking on doors
4. Records what's open, what's closed, and what timed out
5. Spits out results in whatever format you want

It's not rocket science, just good old TCP connections.

## When You Can Actually Use This

- Your own network (obviously)
- Authorized pentesting gigs with a signed contract
- CTF challenges and hacking labs
- Bug bounty programs that explicitly allow it
- Your home lab when you're learning
- Never on production systems you don't own

Basically: if you have to ask "can I scan this?", the answer is probably no.

## Contributing

Found a bug? Want to add features? Cool.

1. Fork it
2. Make your changes
3. Test them (seriously, test them)
4. Submit a PR

Keep it clean, keep it simple.

## License

MIT License. Do whatever you want with it, just don't blame me if things go south.

## Final Word

This tool does exactly what it says on the tin. No backdoors, no phone-home nonsense, just a simple port scanner.

Use it responsibly. Don't scan random targets. Don't be stupid. Stay legal.

If you get yourself in trouble with this, that's a you problem. I gave you the disclaimer, you chose to ignore it.

---

Built for learning, testing, and the occasional "wait, what ports are open on that box again?"
