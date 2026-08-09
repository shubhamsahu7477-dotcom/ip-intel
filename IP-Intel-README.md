# 🌐 IP Intel — Advanced IP Intelligence Tool

A fast, terminal-based **IP intelligence and geolocation tool** written in Python. Look up geolocation, ISP/ASN, network type, VPN/proxy detection, and abuse risk score for any IP address — single lookups or bulk scans, right from your terminal. Fully Termux-compatible — no browser required.

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat&logo=python&logoColor=white)
![Termux](https://img.shields.io/badge/Termux-Compatible-black?style=flat&logo=android&logoColor=green)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> ⚠️ **For ethical, legal use only.** This tool queries only publicly available IP data via third-party APIs (ip-api.com, ipinfo.io, AbuseIPDB). Always respect the terms of service of those APIs and use responsibly. See [Disclaimer](#️-disclaimer--legal-notice).

---

## ✨ Features

- 📍 **Geolocation lookup** — country, region, city, postal code, coordinates, timezone, Google Maps link
- 🏢 **Network info** — ISP, organization, ASN, ASN owner, reverse DNS, network type (Residential/Mobile/Hosting)
- 🛡️ **Security analysis** — VPN/Proxy detection, mobile network detection, hosting/datacenter detection
- ⚠️ **Abuse risk scoring** — combines proxy/hosting signals with AbuseIPDB confidence score and report count into a 0–100 risk score (Minimal / Low / Medium / High)
- 📦 **Bulk IP scanning** — scan multiple IPs at once (manual comma-separated list or from a file)
- 📊 **Bulk summary table** — clean tabular overview of all scanned IPs with country, city, ISP, risk, and VPN status
- 💾 **Export results** — save lookups as `.json` or `.csv`
- 🔑 **Optional AbuseIPDB integration** — add your free API key for abuse confidence scores and report history
- 🎨 **Rich terminal UI** — colorized tables and panels via [`rich`](https://github.com/Textualize/rich), with a plain-text fallback if not installed
- 📱 **Termux-ready** — runs directly on Android terminal, no GUI/browser needed

---

## 🖥️ Preview

```
MENU
  [1] Single IP Lookup
  [2] Bulk IP Scan (multiple IPs)
  [3] Bulk from file (ip_list.txt)
  [4] Set AbuseIPDB API Key
  [5] Exit

Choice:
```

Sample single-lookup output includes sections for **LOCATION**, **NETWORK**, and **SECURITY** — each with clearly color-coded values (green = safe, yellow = caution, red = risk).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation

```bash
git clone https://github.com/<your-username>/ip-intel.git
cd ip-intel
pip install -r requirements.txt
```

### Usage

```bash
python3 ip_intel.py
```

Then choose from the menu:
1. **Single IP Lookup** — enter one IP for a full report
2. **Bulk IP Scan** — enter comma-separated IPs
3. **Bulk from file** — reads IPs line-by-line from `ip_list.txt`
4. **Set AbuseIPDB API Key** — enables abuse-confidence scoring (optional, [get a free key here](https://www.abuseipdb.com/account/api))
5. **Exit**

### 📱 Termux (Android)

```bash
pkg install python -y
pip install -r requirements.txt
python ip_intel.py
```

---

## 🔑 AbuseIPDB API Key (Optional)

To enable abuse-confidence scoring:
1. Create a free account at [abuseipdb.com](https://www.abuseipdb.com/)
2. Generate an API key
3. Run the tool → choose option `[4]` → paste your key

The key is stored locally in a `.abuse_key` file (not committed to version control — see `.gitignore`).

---

## 🛠️ Tech Stack

- **Python 3** — core language
- [`requests`](https://pypi.org/project/requests/) — API calls to ip-api.com, ipinfo.io, AbuseIPDB
- [`rich`](https://pypi.org/project/rich/) — terminal tables, panels, spinners
- Built-in `socket`, `concurrent.futures`, `csv`, `json` — reverse DNS, parallel fetching, export

---

## 📂 Project Structure

```
ip-intel/
├── ip_intel.py         # Main CLI application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## ⚠️ Disclaimer & Legal Notice

This tool is intended **strictly for educational purposes, personal network diagnostics, and authorized security research**.

- Only public IP metadata (geolocation, ASN, abuse reports) is queried — no exploitation or intrusive scanning is performed.
- Respect the rate limits and terms of service of the underlying APIs (ip-api.com, ipinfo.io, AbuseIPDB).
- The author(s) are **not responsible** for any misuse of this tool.

Use responsibly. 🕊️

---

## 📄 License

All Rights Reserved — see [`LICENSE`](LICENSE) for full terms. This project may be used for personal purposes, but copying, modifying, or redistributing the code without permission is not allowed.

---

## 🙋 Author

Made with ❤️ by **[Your Name]**
If this tool helped you, consider giving it a ⭐ on GitHub!
