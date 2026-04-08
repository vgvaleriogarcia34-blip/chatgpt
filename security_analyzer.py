#!/usr/bin/env python3
"""
=============================================================
  ANALIZADOR DE SEGURIDAD WEB Y RED - v1.0
  Ejecuta este script en tu máquina local para obtener
  un análisis completo de seguridad.
=============================================================
Uso: python3 security_analyzer.py [URL_de_tu_web]
Ejemplo: python3 security_analyzer.py https://midominio.com
"""

import subprocess
import sys
import json
import ssl
import socket
import urllib.request
import urllib.error
import re
from datetime import datetime, timezone
from collections import OrderedDict


# ─── COLORES PARA TERMINAL ───────────────────────────────────
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════╗
║        ANALIZADOR DE SEGURIDAD WEB Y RED v1.0           ║
║                                                          ║
║  Analiza: SSL/TLS, Headers HTTP, Puertos, Red Local      ║
╚══════════════════════════════════════════════════════════╝
{Colors.RESET}""")


def score_label(score):
    if score >= 80:
        return f"{Colors.GREEN}ALTO ({score}/100){Colors.RESET}"
    elif score >= 50:
        return f"{Colors.YELLOW}MEDIO ({score}/100){Colors.RESET}"
    else:
        return f"{Colors.RED}BAJO ({score}/100){Colors.RESET}"


# ─── 1. INFORMACIÓN DE RED LOCAL ─────────────────────────────
def analyze_network():
    print(f"\n{Colors.BOLD}{Colors.BLUE}[1/5] ANÁLISIS DE RED LOCAL{Colors.RESET}")
    print("=" * 55)
    results = {"score": 0, "findings": []}

    # IP pública
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5) as resp:
            data = json.loads(resp.read().decode())
            ip = data.get("ip", "Desconocida")
            print(f"  {Colors.CYAN}IP Pública:{Colors.RESET} {ip}")
            results["public_ip"] = ip
    except Exception:
        print(f"  {Colors.YELLOW}IP Pública: No se pudo obtener{Colors.RESET}")
        results["public_ip"] = "N/A"

    # IP local
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"  {Colors.CYAN}IP Local:{Colors.RESET} {local_ip}")
        results["local_ip"] = local_ip
    except Exception:
        print(f"  {Colors.YELLOW}IP Local: No se pudo obtener{Colors.RESET}")

    # Gateway
    try:
        if sys.platform == "darwin":
            out = subprocess.check_output(["route", "-n", "get", "default"],
                                          stderr=subprocess.DEVNULL, text=True)
            for line in out.splitlines():
                if "gateway" in line:
                    gw = line.split(":")[-1].strip()
                    print(f"  {Colors.CYAN}Gateway:{Colors.RESET} {gw}")
        else:
            out = subprocess.check_output(["ip", "route"], stderr=subprocess.DEVNULL, text=True)
            for line in out.splitlines():
                if line.startswith("default"):
                    gw = line.split()[2]
                    print(f"  {Colors.CYAN}Gateway:{Colors.RESET} {gw}")
    except Exception:
        pass

    # DNS
    try:
        with open("/etc/resolv.conf") as f:
            dns_servers = [l.split()[1] for l in f if l.startswith("nameserver")]
            print(f"  {Colors.CYAN}Servidores DNS:{Colors.RESET} {', '.join(dns_servers)}")
            known_secure = {"8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1",
                            "9.9.9.9", "208.67.222.222", "208.67.220.220"}
            if any(d in known_secure for d in dns_servers):
                print(f"    {Colors.GREEN}✓ Usas servidores DNS públicos conocidos{Colors.RESET}")
                results["score"] += 10
            else:
                print(f"    {Colors.YELLOW}⚠ DNS del ISP - considera cambiar a 1.1.1.1 o 8.8.8.8{Colors.RESET}")
                results["findings"].append("Cambiar DNS a proveedores seguros (1.1.1.1 / 8.8.8.8)")
    except Exception:
        pass

    # Verificar si hay WiFi
    try:
        if sys.platform == "darwin":
            wifi_out = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework"
                 "/Versions/Current/Resources/airport", "-I"],
                stderr=subprocess.DEVNULL, text=True)
            for line in wifi_out.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    print(f"  {Colors.CYAN}Red WiFi:{Colors.RESET} {line.split(':')[-1].strip()}")
                if "link auth" in line.lower():
                    auth = line.split(":")[-1].strip()
                    print(f"  {Colors.CYAN}Autenticación:{Colors.RESET} {auth}")
                    if "wpa3" in auth.lower():
                        print(f"    {Colors.GREEN}✓ WPA3 - Excelente seguridad WiFi{Colors.RESET}")
                        results["score"] += 20
                    elif "wpa2" in auth.lower():
                        print(f"    {Colors.GREEN}✓ WPA2 - Buena seguridad WiFi{Colors.RESET}")
                        results["score"] += 15
                    elif "wep" in auth.lower():
                        print(f"    {Colors.RED}✗ WEP - INSEGURO, cambiar inmediatamente{Colors.RESET}")
                        results["findings"].append("CRÍTICO: Cambiar cifrado WiFi de WEP a WPA2/WPA3")
        else:
            try:
                wifi_out = subprocess.check_output(["iwconfig"],
                                                   stderr=subprocess.DEVNULL, text=True)
                for line in wifi_out.splitlines():
                    if "ESSID" in line:
                        ssid = re.search(r'ESSID:"([^"]*)"', line)
                        if ssid:
                            print(f"  {Colors.CYAN}Red WiFi:{Colors.RESET} {ssid.group(1)}")
                    if "Encryption key" in line:
                        if "on" in line.lower():
                            print(f"    {Colors.GREEN}✓ Cifrado activado{Colors.RESET}")
                            results["score"] += 10
                        else:
                            print(f"    {Colors.RED}✗ Sin cifrado WiFi{Colors.RESET}")
                            results["findings"].append("CRÍTICO: WiFi sin cifrado")
            except FileNotFoundError:
                try:
                    wifi_out = subprocess.check_output(
                        ["nmcli", "-t", "-f", "ACTIVE,SSID,SECURITY", "dev", "wifi"],
                        stderr=subprocess.DEVNULL, text=True)
                    for line in wifi_out.splitlines():
                        if line.startswith("yes:") or line.startswith("sí:"):
                            parts = line.split(":")
                            if len(parts) >= 3:
                                print(f"  {Colors.CYAN}Red WiFi:{Colors.RESET} {parts[1]}")
                                sec = parts[2]
                                print(f"  {Colors.CYAN}Seguridad:{Colors.RESET} {sec}")
                                if "WPA3" in sec:
                                    print(f"    {Colors.GREEN}✓ WPA3 - Excelente{Colors.RESET}")
                                    results["score"] += 20
                                elif "WPA2" in sec:
                                    print(f"    {Colors.GREEN}✓ WPA2 - Buena{Colors.RESET}")
                                    results["score"] += 15
                                elif "WEP" in sec:
                                    print(f"    {Colors.RED}✗ WEP - INSEGURO{Colors.RESET}")
                                    results["findings"].append("CRÍTICO: WEP es inseguro")
                except FileNotFoundError:
                    print(f"  {Colors.YELLOW}⚠ No se pudo detectar info WiFi (instala nmcli o iwconfig){Colors.RESET}")
    except Exception:
        print(f"  {Colors.YELLOW}⚠ Info WiFi no disponible en este sistema{Colors.RESET}")

    results["score"] = min(results["score"], 20)
    return results


# ─── 2. ANÁLISIS SSL/TLS ─────────────────────────────────────
def analyze_ssl(hostname):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[2/5] ANÁLISIS SSL/TLS - {hostname}{Colors.RESET}")
    print("=" * 55)
    results = {"score": 0, "findings": []}

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                protocol = ssock.version()

                # Protocolo
                print(f"  {Colors.CYAN}Protocolo:{Colors.RESET} {protocol}")
                if "TLSv1.3" in protocol:
                    print(f"    {Colors.GREEN}✓ TLS 1.3 - Máxima seguridad{Colors.RESET}")
                    results["score"] += 10
                elif "TLSv1.2" in protocol:
                    print(f"    {Colors.GREEN}✓ TLS 1.2 - Aceptable{Colors.RESET}")
                    results["score"] += 7
                else:
                    print(f"    {Colors.RED}✗ Protocolo obsoleto - ACTUALIZAR{Colors.RESET}")
                    results["findings"].append(f"Actualizar de {protocol} a TLS 1.2+")

                # Cipher
                cipher = ssock.cipher()
                if cipher:
                    print(f"  {Colors.CYAN}Cipher:{Colors.RESET} {cipher[0]}")
                    if "AES" in cipher[0] and ("GCM" in cipher[0] or "CHACHA" in cipher[0].upper()):
                        print(f"    {Colors.GREEN}✓ Cipher fuerte{Colors.RESET}")
                        results["score"] += 5
                    results["score"] += 3

                # Certificado
                subject = dict(x[0] for x in cert.get("subject", []))
                issuer = dict(x[0] for x in cert.get("issuer", []))
                not_after = cert.get("notAfter", "")

                print(f"  {Colors.CYAN}Dominio:{Colors.RESET} {subject.get('commonName', 'N/A')}")
                print(f"  {Colors.CYAN}Emisor:{Colors.RESET} {issuer.get('organizationName', 'N/A')}")
                print(f"  {Colors.CYAN}Expira:{Colors.RESET} {not_after}")

                # Verificar expiración
                if not_after:
                    try:
                        exp_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                        exp_date = exp_date.replace(tzinfo=timezone.utc)
                        now = datetime.now(timezone.utc)
                        days_left = (exp_date - now).days
                        if days_left > 30:
                            print(f"    {Colors.GREEN}✓ Certificado válido ({days_left} días restantes){Colors.RESET}")
                            results["score"] += 5
                        elif days_left > 0:
                            print(f"    {Colors.YELLOW}⚠ Certificado expira pronto ({days_left} días){Colors.RESET}")
                            results["findings"].append(f"Renovar certificado SSL ({days_left} días restantes)")
                            results["score"] += 2
                        else:
                            print(f"    {Colors.RED}✗ CERTIFICADO EXPIRADO{Colors.RESET}")
                            results["findings"].append("CRÍTICO: Certificado SSL expirado")
                    except ValueError:
                        pass

                # SANs
                san = cert.get("subjectAltName", [])
                if san:
                    domains = [x[1] for x in san if x[0] == "DNS"]
                    print(f"  {Colors.CYAN}Dominios cubiertos:{Colors.RESET} {', '.join(domains[:5])}")

    except ssl.SSLError as e:
        print(f"  {Colors.RED}✗ Error SSL: {e}{Colors.RESET}")
        results["findings"].append(f"Error SSL: {e}")
    except socket.timeout:
        print(f"  {Colors.RED}✗ Timeout al conectar al puerto 443{Colors.RESET}")
        results["findings"].append("No se pudo conectar al puerto 443 (HTTPS)")
    except ConnectionRefusedError:
        print(f"  {Colors.RED}✗ Conexión rechazada en puerto 443{Colors.RESET}")
        results["findings"].append("Puerto 443 (HTTPS) cerrado o no disponible")
    except Exception as e:
        print(f"  {Colors.RED}✗ Error: {e}{Colors.RESET}")
        results["findings"].append(f"Error en análisis SSL: {e}")

    results["score"] = min(results["score"], 25)
    return results


# ─── 3. ANÁLISIS DE HEADERS HTTP ─────────────────────────────
def analyze_headers(url):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[3/5] ANÁLISIS DE HEADERS DE SEGURIDAD HTTP{Colors.RESET}")
    print("=" * 55)
    results = {"score": 0, "findings": []}

    security_headers = OrderedDict([
        ("Strict-Transport-Security", {
            "desc": "HSTS - Fuerza HTTPS",
            "critical": True,
            "points": 5,
        }),
        ("Content-Security-Policy", {
            "desc": "CSP - Previene XSS",
            "critical": True,
            "points": 5,
        }),
        ("X-Content-Type-Options", {
            "desc": "Previene MIME sniffing",
            "critical": False,
            "points": 3,
        }),
        ("X-Frame-Options", {
            "desc": "Previene clickjacking",
            "critical": False,
            "points": 3,
        }),
        ("X-XSS-Protection", {
            "desc": "Filtro XSS del navegador",
            "critical": False,
            "points": 2,
        }),
        ("Referrer-Policy", {
            "desc": "Controla info del referrer",
            "critical": False,
            "points": 2,
        }),
        ("Permissions-Policy", {
            "desc": "Controla APIs del navegador",
            "critical": False,
            "points": 2,
        }),
        ("X-Permitted-Cross-Domain-Policies", {
            "desc": "Políticas cross-domain",
            "critical": False,
            "points": 1,
        }),
    ])

    dangerous_headers = ["Server", "X-Powered-By", "X-AspNet-Version", "X-AspNetMvc-Version"]

    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "SecurityAnalyzer/1.0")
        with urllib.request.urlopen(req, timeout=10) as resp:
            headers = dict(resp.headers)

            # Verificar headers de seguridad presentes
            print(f"\n  {Colors.BOLD}Headers de seguridad:{Colors.RESET}")
            for header, info in security_headers.items():
                found = None
                for h in headers:
                    if h.lower() == header.lower():
                        found = headers[h]
                        break
                if found:
                    print(f"    {Colors.GREEN}✓ {header}{Colors.RESET}: {found[:60]}")
                    results["score"] += info["points"]
                else:
                    icon = "✗" if info["critical"] else "⚠"
                    color = Colors.RED if info["critical"] else Colors.YELLOW
                    print(f"    {color}{icon} {header}{Colors.RESET} - FALTA ({info['desc']})")
                    priority = "CRÍTICO" if info["critical"] else "Recomendado"
                    results["findings"].append(f"{priority}: Agregar header {header}")

            # Verificar headers que revelan información
            print(f"\n  {Colors.BOLD}Headers que revelan información:{Colors.RESET}")
            for header in dangerous_headers:
                found = None
                for h in headers:
                    if h.lower() == header.lower():
                        found = headers[h]
                        break
                if found:
                    print(f"    {Colors.RED}✗ {header}: {found}{Colors.RESET} - Ocultar este header")
                    results["findings"].append(f"Ocultar header {header} ({found})")
                else:
                    print(f"    {Colors.GREEN}✓ {header}: No expuesto{Colors.RESET}")
                    results["score"] += 1

    except urllib.error.HTTPError as e:
        print(f"  {Colors.YELLOW}⚠ HTTP {e.code}: {e.reason}{Colors.RESET}")
    except Exception as e:
        print(f"  {Colors.RED}✗ Error: {e}{Colors.RESET}")
        results["findings"].append(f"Error al analizar headers: {e}")

    results["score"] = min(results["score"], 25)
    return results


# ─── 4. PUERTOS COMUNES ──────────────────────────────────────
def analyze_ports(hostname):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[4/5] ESCANEO DE PUERTOS COMUNES - {hostname}{Colors.RESET}")
    print("=" * 55)
    results = {"score": 15, "findings": []}

    common_ports = {
        21: ("FTP", True),
        22: ("SSH", False),
        23: ("Telnet", True),
        25: ("SMTP", False),
        53: ("DNS", False),
        80: ("HTTP", False),
        110: ("POP3", True),
        143: ("IMAP", True),
        443: ("HTTPS", False),
        445: ("SMB", True),
        993: ("IMAPS", False),
        995: ("POP3S", False),
        3306: ("MySQL", True),
        3389: ("RDP", True),
        5432: ("PostgreSQL", True),
        5900: ("VNC", True),
        6379: ("Redis", True),
        8080: ("HTTP-Alt", False),
        8443: ("HTTPS-Alt", False),
        27017: ("MongoDB", True),
    }

    open_ports = []
    risky_ports = []

    for port, (service, risky) in sorted(common_ports.items()):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((hostname, port))
            sock.close()
            if result == 0:
                open_ports.append((port, service))
                if risky:
                    risky_ports.append((port, service))
                    print(f"    {Colors.RED}✗ Puerto {port} ({service}) - ABIERTO (RIESGO){Colors.RESET}")
                    results["score"] -= 3
                    results["findings"].append(
                        f"Puerto {port} ({service}) abierto - Considerar cerrar")
                else:
                    print(f"    {Colors.GREEN}● Puerto {port} ({service}) - ABIERTO{Colors.RESET}")
        except Exception:
            pass

    if not open_ports:
        print(f"  {Colors.GREEN}✓ No se encontraron puertos abiertos (o filtrados){Colors.RESET}")
    else:
        print(f"\n  Total puertos abiertos: {len(open_ports)}")
        if risky_ports:
            print(f"  {Colors.RED}Puertos de riesgo: {len(risky_ports)}{Colors.RESET}")

    results["score"] = max(results["score"], 0)
    results["score"] = min(results["score"], 15)
    return results


# ─── 5. VERIFICACIONES ADICIONALES ───────────────────────────
def analyze_extras(url, hostname):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[5/5] VERIFICACIONES ADICIONALES{Colors.RESET}")
    print("=" * 55)
    results = {"score": 0, "findings": []}

    # Redirección HTTP -> HTTPS
    try:
        http_url = url.replace("https://", "http://")
        req = urllib.request.Request(http_url, method="HEAD")
        req.add_header("User-Agent", "SecurityAnalyzer/1.0")
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        resp = opener.open(req, timeout=5)
        final_url = resp.geturl()
        if final_url.startswith("https://"):
            print(f"  {Colors.GREEN}✓ Redirección HTTP → HTTPS activa{Colors.RESET}")
            results["score"] += 5
        else:
            print(f"  {Colors.RED}✗ Sin redirección a HTTPS{Colors.RESET}")
            results["findings"].append("Configurar redirección HTTP → HTTPS")
    except Exception:
        print(f"  {Colors.YELLOW}⚠ No se pudo verificar redirección HTTP → HTTPS{Colors.RESET}")

    # DNSSEC
    try:
        out = subprocess.check_output(["dig", "+short", hostname, "DNSKEY"],
                                      stderr=subprocess.DEVNULL, text=True, timeout=5)
        if out.strip():
            print(f"  {Colors.GREEN}✓ DNSSEC configurado{Colors.RESET}")
            results["score"] += 5
        else:
            print(f"  {Colors.YELLOW}⚠ DNSSEC no detectado{Colors.RESET}")
            results["findings"].append("Considerar activar DNSSEC")
    except Exception:
        print(f"  {Colors.YELLOW}⚠ No se pudo verificar DNSSEC{Colors.RESET}")

    # Cookies
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "SecurityAnalyzer/1.0")
        with urllib.request.urlopen(req, timeout=10) as resp:
            cookies = [v for k, v in resp.headers.items() if k.lower() == "set-cookie"]
            if cookies:
                print(f"\n  {Colors.BOLD}Cookies detectadas:{Colors.RESET}")
                for cookie in cookies[:5]:
                    flags = []
                    if "secure" in cookie.lower():
                        flags.append(f"{Colors.GREEN}Secure{Colors.RESET}")
                    else:
                        flags.append(f"{Colors.RED}No-Secure{Colors.RESET}")
                        results["findings"].append("Cookie sin flag Secure")
                    if "httponly" in cookie.lower():
                        flags.append(f"{Colors.GREEN}HttpOnly{Colors.RESET}")
                    else:
                        flags.append(f"{Colors.RED}No-HttpOnly{Colors.RESET}")
                        results["findings"].append("Cookie sin flag HttpOnly")
                    if "samesite" in cookie.lower():
                        flags.append(f"{Colors.GREEN}SameSite{Colors.RESET}")
                    else:
                        flags.append(f"{Colors.YELLOW}No-SameSite{Colors.RESET}")

                    name = cookie.split("=")[0].strip()
                    print(f"    {name}: {' | '.join(flags)}")
                    results["score"] += 2
            else:
                print(f"  {Colors.CYAN}No se detectaron cookies{Colors.RESET}")
                results["score"] += 5
    except Exception:
        pass

    results["score"] = min(results["score"], 15)
    return results


# ─── REPORTE FINAL ────────────────────────────────────────────
def generate_report(scores, url):
    print(f"\n\n{Colors.BOLD}{Colors.MAGENTA}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              REPORTE FINAL DE SEGURIDAD                 ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(Colors.RESET)

    total = 0
    max_total = 100
    categories = [
        ("Red Local / WiFi", scores.get("network", {})),
        ("SSL/TLS", scores.get("ssl", {})),
        ("Headers HTTP", scores.get("headers", {})),
        ("Puertos", scores.get("ports", {})),
        ("Verificaciones Extra", scores.get("extras", {})),
    ]

    for name, data in categories:
        s = data.get("score", 0)
        total += s
        bar_len = int(s / 25 * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {name:.<30} [{bar}] {s} pts")

    print(f"\n  {Colors.BOLD}PUNTUACIÓN TOTAL: {score_label(total)}{Colors.RESET}")
    print()

    # Todas las findings
    all_findings = []
    for _, data in categories:
        all_findings.extend(data.get("findings", []))

    if all_findings:
        print(f"  {Colors.BOLD}{Colors.RED}HALLAZGOS Y RECOMENDACIONES:{Colors.RESET}")
        critical = [f for f in all_findings if "CRÍTICO" in f]
        important = [f for f in all_findings if "CRÍTICO" not in f]

        if critical:
            print(f"\n  {Colors.RED}  ◆ CRÍTICOS:{Colors.RESET}")
            for f in critical:
                print(f"    {Colors.RED}  → {f}{Colors.RESET}")
        if important:
            print(f"\n  {Colors.YELLOW}  ◆ RECOMENDADOS:{Colors.RESET}")
            for f in important:
                print(f"    {Colors.YELLOW}  → {f}{Colors.RESET}")
    else:
        print(f"  {Colors.GREEN}✓ No se encontraron problemas significativos{Colors.RESET}")

    print(f"\n  {Colors.CYAN}Análisis completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"  {Colors.CYAN}Objetivo: {url}{Colors.RESET}")
    print()


# ─── MAIN ─────────────────────────────────────────────────────
def main():
    banner()

    if len(sys.argv) < 2:
        print(f"  {Colors.YELLOW}Uso: python3 security_analyzer.py <URL>{Colors.RESET}")
        print(f"  {Colors.YELLOW}Ejemplo: python3 security_analyzer.py https://midominio.com{Colors.RESET}")
        print()

        # Solo análisis de red si no se da URL
        print(f"  {Colors.CYAN}Ejecutando solo análisis de red local...{Colors.RESET}")
        network_results = analyze_network()
        scores = {"network": network_results}
        print(f"\n  {Colors.BOLD}Para un análisis completo, proporciona la URL de tu web.{Colors.RESET}")
        return

    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url

    # Extraer hostname
    hostname = url.split("//")[-1].split("/")[0].split(":")[0]
    print(f"  {Colors.CYAN}Objetivo: {url}{Colors.RESET}")
    print(f"  {Colors.CYAN}Host: {hostname}{Colors.RESET}")

    scores = {}

    # Ejecutar todos los análisis
    scores["network"] = analyze_network()
    scores["ssl"] = analyze_ssl(hostname)
    scores["headers"] = analyze_headers(url)
    scores["ports"] = analyze_ports(hostname)
    scores["extras"] = analyze_extras(url, hostname)

    # Generar reporte
    generate_report(scores, url)


if __name__ == "__main__":
    main()
