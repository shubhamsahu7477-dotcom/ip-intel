# IP Intel v2.0 — Advanced Terminal Tool

Termux pe seedha chalao, browser ki zaroorat nahi!

## Installation (Termux)

```bash
pkg update && pkg upgrade -y
pkg install python -y
pip install requests rich
```

## Run karo

```bash
python ip_intel.py
```

## Features

- Single IP full details
- Bulk scan (multiple IPs ek saath)
- File se IPs load karo (ip_list.txt)
- Location, Network, Security info
- VPN/Proxy detection
- Risk score (0-100)
- JSON / CSV export
- AbuseIPDB integration (optional)

## Bulk file format (ip_list.txt)

```
8.8.8.8
1.1.1.1
# comment line ignore hogi
142.250.180.46
```

## AbuseIPDB Key (optional)

Free key: https://www.abuseipdb.com/register
Menu mein [4] se set karo.

⚠️ Key `.abuse_key` file mein plaintext mein save hoti hai (script ke folder mein). Yeh file `.gitignore` mein already excluded hai — kabhi bhi GitHub pe commit mat karna.

## Disclaimer

Yeh tool sirf publicly available geolocation/network data (ip-api.com, ipinfo.io, AbuseIPDB) dikhata hai — koi private ya hacked data nahi. Apni jurisdiction ke privacy/cybersecurity laws follow karke hi use karo. Kisi ke against harassment ya stalking ke liye use mat karo.

## License

MIT — dekho [LICENSE](LICENSE)
