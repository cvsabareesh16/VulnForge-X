import subprocess, shutil, requests
from core.utils import normalize_target, resolve_ip, save_json, timestamp, safe_filename, SCAN_DIR, ensure_dirs
from core.colors import C

COMMON_PORTS = ['21','22','25','53','80','110','139','143','443','445','3306','3389','5432','8080']

def run_recon(target):
    host = normalize_target(target)
    ip = resolve_ip(host)
    result = {'target': host, 'ip': ip, 'timestamp': timestamp(), 'http': {}, 'nmap': {}, 'open_ports': []}
    print(C.BLUE + f"[+] Target: {host}\n[+] IP: {ip}" + C.RESET)

    for scheme in ['https','http']:
        try:
            r = requests.get(f'{scheme}://{host}', timeout=5, allow_redirects=True)
            result['http'][scheme] = {'status': r.status_code, 'server': r.headers.get('Server','Unknown'), 'url': r.url}
            print(C.GREEN + f"[+] {scheme.upper()} reachable: {r.status_code}" + C.RESET)
        except Exception as e:
            result['http'][scheme] = {'error': str(e)}

    if shutil.which('nmap'):
        try:
            cmd = ['nmap','-sV','-Pn','--top-ports','100',host]
            print(C.YELLOW + '[+] Running safe Nmap version scan...' + C.RESET)
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=180)
            result['nmap']['raw'] = out
            for line in out.splitlines():
                if '/tcp' in line and 'open' in line:
                    result['open_ports'].append(line.strip())
            print(C.GREEN + f"[✓] Open services found: {len(result['open_ports'])}" + C.RESET)
        except Exception as e:
            result['nmap']['error'] = str(e)
            print(C.RED + f"[!] Nmap error: {e}" + C.RESET)
    else:
        result['nmap']['note'] = 'Nmap not installed. Install with: sudo apt install nmap'
        print(C.YELLOW + '[!] Nmap not found. Skipping Nmap scan.' + C.RESET)

    ensure_dirs()
    path = f"{SCAN_DIR}/{safe_filename(host)}_{result['timestamp']}/recon.json"
    save_json(path, result)
    print(C.GREEN + f"[✓] Saved: {path}" + C.RESET)
    return result, path
