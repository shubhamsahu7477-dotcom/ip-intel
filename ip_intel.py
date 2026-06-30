#!/usr/bin/env python3
"""
IP Intel Advanced — Terminal Tool
Termux pe seedha chalao, browser ki zaroorat nahi
"""

import requests
import socket
import json
import csv
import sys
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.text import Text
    from rich.rule import Rule
    from rich import box
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH = True
    console = Console()
except ImportError:
    RICH = False
    console = None

TIMEOUT = 8

# ─── Colors (fallback without rich) ────────────────────────────────────────────
def c(text, color=None):
    if RICH:
        return text
    codes = {'cyan':'\033[96m','green':'\033[92m','red':'\033[91m',
             'yellow':'\033[93m','blue':'\033[94m','magenta':'\033[95m',
             'bold':'\033[1m','dim':'\033[2m','reset':'\033[0m'}
    if color and color in codes:
        return f"{codes[color]}{text}{codes['reset']}"
    return text

def banner():
    b = """
╔══════════════════════════════════════════════════════╗
║  ██╗██████╗     ██╗███╗   ██╗████████╗███████╗██╗  ║
║  ██║██╔══██╗    ██║████╗  ██║╚══██╔══╝██╔════╝██║  ║
║  ██║██████╔╝    ██║██╔██╗ ██║   ██║   █████╗  ██║  ║
║  ██║██╔═══╝     ██║██║╚██╗██║   ██║   ██╔══╝  ██║  ║
║  ██║██║         ██║██║ ╚████║   ██║   ███████╗██║  ║
║  ╚═╝╚═╝         ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ║
║                                                      ║
║         Advanced IP Intelligence Tool v2.0           ║
║      Termux Terminal — No Browser Required           ║
╚══════════════════════════════════════════════════════╝"""
    if RICH:
        console.print(b, style="cyan")
    else:
        print(c(b, 'cyan'))

# ─── API Functions ──────────────────────────────────────────────────────────────
def fetch_ipapi(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        r = requests.get(url, timeout=TIMEOUT)
        d = r.json()
        if d.get('status') == 'success':
            return {'ok': True, 'data': d}
    except Exception:
        pass
    return {'ok': False}

def fetch_ipinfo(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=TIMEOUT)
        d = r.json()
        if 'ip' in d:
            return {'ok': True, 'data': d}
    except Exception:
        pass
    return {'ok': False}

def fetch_abuseipdb(ip, api_key=''):
    if not api_key:
        return {'ok': False, 'reason': 'no_key'}
    try:
        r = requests.get("https://api.abuseipdb.com/api/v2/check",
                         headers={'Key': api_key, 'Accept': 'application/json'},
                         params={'ipAddress': ip, 'maxAgeInDays': 90},
                         timeout=TIMEOUT)
        d = r.json()
        if 'data' in d:
            return {'ok': True, 'data': d['data']}
    except Exception:
        pass
    return {'ok': False}

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return 'N/A'

def get_risk(proxy, hosting, abuse_score=0):
    score = 0
    if proxy:
        score += 35
    if hosting:
        score += 15
    score += int(abuse_score * 0.5)
    score = min(score, 100)
    if score >= 70:
        return score, 'HIGH', 'red'
    elif score >= 40:
        return score, 'MEDIUM', 'yellow'
    elif score >= 15:
        return score, 'LOW', 'blue'
    return score, 'MINIMAL', 'green'

# ─── Display Functions ──────────────────────────────────────────────────────────
def print_section(title):
    if RICH:
        console.print(Rule(f"[bold cyan] {title} [/bold cyan]", style="cyan"))
    else:
        print(f"\n{'─'*50}")
        print(c(f"  {title}", 'cyan'))
        print('─'*50)

def print_row(label, value, val_color='white'):
    if RICH:
        console.print(f"  [dim]{label:<22}[/dim] [bold {val_color}]{value}[/bold {val_color}]")
    else:
        print(f"  {c(label+':', 'dim'):<24} {c(str(value), val_color)}")

def print_ip_result(ip, data, abuse_data=None):
    ipapi = data.get('ipapi', {})
    ipinfo = data.get('ipinfo', {})

    country = ipapi.get('country', '') or ipinfo.get('country', '') or 'Unknown'
    country_code = ipapi.get('countryCode', '') or ''
    region = ipapi.get('regionName', '') or ''
    city = ipapi.get('city', '') or ipinfo.get('city', '') or ''
    postal = ipapi.get('zip', '') or ipinfo.get('postal', '') or 'N/A'
    lat = ipapi.get('lat', '') or ''
    lon = ipapi.get('lon', '') or ''
    timezone = ipapi.get('timezone', '') or ''
    isp = ipapi.get('isp', '') or ipinfo.get('org', '') or 'Unknown'
    org = ipapi.get('org', '') or 'Unknown'
    asn = ipapi.get('as', '') or ''
    asn_name = ipapi.get('asname', '') or ''
    rdns = reverse_dns(ip)
    is_proxy = bool(ipapi.get('proxy'))
    is_mobile = bool(ipapi.get('mobile'))
    is_hosting = bool(ipapi.get('hosting'))

    abuse_score = abuse_data.get('abuseConfidenceScore', 0) if abuse_data else 0
    total_reports = abuse_data.get('totalReports', 0) if abuse_data else 0

    risk_score, risk_level, risk_color = get_risk(is_proxy, is_hosting, abuse_score)

    maps = f"https://maps.google.com/?q={lat},{lon}" if lat and lon else 'N/A'

    if RICH:
        console.print(f"\n[bold cyan]━━━ IP: {ip} ━━━[/bold cyan]")
    else:
        print(f"\n{c('━'*40, 'cyan')}")
        print(c(f"  IP: {ip}", 'cyan bold'))

    print_section("LOCATION")
    print_row("Country", f"{country} ({country_code})", 'white')
    print_row("Region", region or 'N/A')
    print_row("City", city or 'N/A')
    print_row("Postal Code", postal)
    print_row("Coordinates", f"{lat}, {lon}" if lat else 'N/A')
    print_row("Timezone", timezone or 'N/A')
    print_row("Google Maps", maps, 'blue')

    print_section("NETWORK")
    print_row("ISP", isp)
    print_row("Organization", org)
    print_row("ASN", asn)
    print_row("ASN Owner", asn_name)
    print_row("Reverse DNS", rdns)
    net_type = 'Mobile' if is_mobile else ('Hosting/DC' if is_hosting else 'Residential')
    print_row("Network Type", net_type)

    print_section("SECURITY")
    print_row("VPN / Proxy", 'YES ⚠' if is_proxy else 'NO ✓', 'red' if is_proxy else 'green')
    print_row("Mobile Network", 'YES' if is_mobile else 'NO', 'yellow' if is_mobile else 'white')
    print_row("Hosting / DC", 'YES' if is_hosting else 'NO', 'yellow' if is_hosting else 'white')
    print_row("Abuse Score", f"{abuse_score}%", 'red' if abuse_score > 50 else 'yellow' if abuse_score > 0 else 'green')
    print_row("Total Reports", str(total_reports), 'red' if total_reports > 0 else 'green')
    print_row("Risk Score", f"{risk_score}/100", risk_color)
    print_row("Risk Level", risk_level, risk_color)

    if RICH:
        console.print()
    else:
        print()

    return {
        'ip': ip,
        'country': country,
        'country_code': country_code,
        'region': region,
        'city': city,
        'postal': postal,
        'latitude': lat,
        'longitude': lon,
        'timezone': timezone,
        'isp': isp,
        'organization': org,
        'asn': asn,
        'reverse_dns': rdns,
        'network_type': net_type,
        'is_proxy': is_proxy,
        'is_mobile': is_mobile,
        'is_hosting': is_hosting,
        'abuse_score': abuse_score,
        'total_reports': total_reports,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'maps_link': maps,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# ─── Lookup Engine ──────────────────────────────────────────────────────────────
def lookup(ip, abuse_key=''):
    ip = ip.strip()
    if not ip:
        return None

    if RICH:
        with Progress(SpinnerColumn(), TextColumn(f"[cyan]Scanning {ip}..."),
                      transient=True) as prog:
            prog.add_task("scan")
            time.sleep(0.3)

            with ThreadPoolExecutor(max_workers=3) as ex:
                f1 = ex.submit(fetch_ipapi, ip)
                f2 = ex.submit(fetch_ipinfo, ip)
                f3 = ex.submit(fetch_abuseipdb, ip, abuse_key)
                r1 = f1.result()
                r2 = f2.result()
                r3 = f3.result()
    else:
        print(f"[*] Scanning {ip}...")
        with ThreadPoolExecutor(max_workers=3) as ex:
            f1 = ex.submit(fetch_ipapi, ip)
            f2 = ex.submit(fetch_ipinfo, ip)
            f3 = ex.submit(fetch_abuseipdb, ip, abuse_key)
            r1, r2, r3 = f1.result(), f2.result(), f3.result()

    combined = {
        'ipapi': r1['data'] if r1['ok'] else {},
        'ipinfo': r2['data'] if r2['ok'] else {},
    }
    abuse = r3['data'] if r3.get('ok') else None

    return print_ip_result(ip, combined, abuse)

# ─── Bulk Scan ──────────────────────────────────────────────────────────────────
def bulk_scan(ip_list, abuse_key=''):
    results = []
    total = len(ip_list)

    print_section(f"BULK SCAN — {total} IPs")

    for i, ip in enumerate(ip_list, 1):
        if RICH:
            console.print(f"[dim]({i}/{total})[/dim] Scanning [cyan]{ip}[/cyan]...")
        else:
            print(f"({i}/{total}) Scanning {ip}...")

        r = lookup(ip, abuse_key)
        if r:
            results.append(r)
        time.sleep(0.5)  # Rate limit se bachao

    return results

def show_bulk_summary(results):
    if not results:
        return

    print_section("BULK SCAN SUMMARY")

    if RICH:
        table = Table(box=box.ROUNDED, border_style="cyan", header_style="bold cyan")
        table.add_column("IP", style="green bold", min_width=16)
        table.add_column("Country", min_width=14)
        table.add_column("City", min_width=14)
        table.add_column("ISP", min_width=20)
        table.add_column("Risk", min_width=10)
        table.add_column("VPN", min_width=6)

        for r in results:
            risk_color = {'HIGH':'red','MEDIUM':'yellow','LOW':'blue'}.get(r['risk_level'],'green')
            vpn = "[red]YES[/red]" if r['is_proxy'] else "[green]NO[/green]"
            table.add_row(
                r['ip'], r['country'], r['city'],
                r['isp'][:20], f"[{risk_color}]{r['risk_level']}[/{risk_color}]", vpn
            )
        console.print(table)
    else:
        print(f"\n{'IP':<17} {'Country':<14} {'City':<14} {'Risk':<10} {'VPN'}")
        print('─'*65)
        for r in results:
            print(f"{r['ip']:<17} {r['country'][:13]:<14} {r['city'][:13]:<14} {r['risk_level']:<10} {'YES' if r['is_proxy'] else 'NO'}")

# ─── Export ─────────────────────────────────────────────────────────────────────
def export_json(results, ip=''):
    fname = f"ip_intel_{ip.replace('.','_') or 'bulk'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, 'w') as f:
        json.dump(results if isinstance(results, list) else [results], f, indent=2)
    msg = f"[+] JSON saved: {fname}"
    if RICH:
        console.print(f"[green]{msg}[/green]")
    else:
        print(c(msg, 'green'))

def export_csv(results, ip=''):
    fname = f"ip_intel_{ip.replace('.','_') or 'bulk'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    data = results if isinstance(results, list) else [results]
    if not data:
        return
    with open(fname, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    msg = f"[+] CSV saved: {fname}"
    if RICH:
        console.print(f"[green]{msg}[/green]")
    else:
        print(c(msg, 'green'))

# ─── Main Menu ──────────────────────────────────────────────────────────────────
def main():
    banner()

    # AbuseIPDB key (optional)
    abuse_key = ''
    key_file = os.path.join(os.path.dirname(__file__), '.abuse_key')
    if os.path.exists(key_file):
        with open(key_file) as f:
            abuse_key = f.read().strip()

    while True:
        if RICH:
            console.print("\n[bold cyan]MENU[/bold cyan]")
            console.print("  [cyan][1][/cyan] Single IP Lookup")
            console.print("  [cyan][2][/cyan] Bulk IP Scan (multiple IPs)")
            console.print("  [cyan][3][/cyan] Bulk from file (ip_list.txt)")
            console.print("  [cyan][4][/cyan] Set AbuseIPDB API Key")
            console.print("  [cyan][5][/cyan] Exit")
        else:
            print("\nMENU:")
            print("  [1] Single IP Lookup")
            print("  [2] Bulk IP Scan")
            print("  [3] Bulk from file (ip_list.txt)")
            print("  [4] Set AbuseIPDB API Key")
            print("  [5] Exit")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            ip = input("IP address daalo: ").strip()
            result = lookup(ip, abuse_key)
            if result:
                exp = input("Export? (j=JSON / c=CSV / n=Skip): ").strip().lower()
                if exp == 'j':
                    export_json(result, ip)
                elif exp == 'c':
                    export_csv(result, ip)

        elif choice == '2':
            raw = input("IPs daalo (comma se alag karo):\n> ").strip()
            ip_list = [x.strip() for x in raw.split(',') if x.strip()]
            if not ip_list:
                print("[!] Koi IP nahi mila.")
                continue
            results = bulk_scan(ip_list, abuse_key)
            show_bulk_summary(results)
            exp = input("\nExport? (j=JSON / c=CSV / b=Dono / n=Skip): ").strip().lower()
            if exp in ('j', 'b'):
                export_json(results)
            if exp in ('c', 'b'):
                export_csv(results)

        elif choice == '3':
            fname = input("File name [ip_list.txt]: ").strip() or 'ip_list.txt'
            if not os.path.exists(fname):
                print(f"[!] File nahi mili: {fname}")
                print("    Ek file banao jisme har line mein ek IP ho.")
                continue
            with open(fname) as f:
                ip_list = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"[*] {len(ip_list)} IPs file se load hue.")
            results = bulk_scan(ip_list, abuse_key)
            show_bulk_summary(results)
            exp = input("\nExport? (j=JSON / c=CSV / b=Dono / n=Skip): ").strip().lower()
            if exp in ('j', 'b'):
                export_json(results)
            if exp in ('c', 'b'):
                export_csv(results)

        elif choice == '4':
            key = input("AbuseIPDB API Key daalo: ").strip()
            with open(key_file, 'w') as f:
                f.write(key)
            abuse_key = key
            print("[+] Key save ho gai!")

        elif choice == '5':
            print("\nBye! Apna network safe rakho.\n")
            break

        else:
            print("[!] Invalid choice.")

if __name__ == '__main__':
    main()
