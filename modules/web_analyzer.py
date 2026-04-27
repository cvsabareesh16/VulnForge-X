import requests
from urllib.parse import urlparse
from core.utils import normalize_target, save_json, timestamp, safe_filename, SCAN_DIR, ensure_dirs
from core.colors import C

SEC_HEADERS = {
    'Content-Security-Policy': 'Helps reduce XSS impact',
    'X-Frame-Options': 'Helps prevent clickjacking',
    'X-Content-Type-Options': 'Helps prevent MIME sniffing',
    'Strict-Transport-Security': 'Enforces HTTPS',
    'Referrer-Policy': 'Controls referrer leakage'
}
COMMON_PATHS = ['/admin','/login','/backup','/.git/','/phpinfo.php','/robots.txt']

def analyze_web(target):
    host = normalize_target(target)
    base = target if target.startswith(('http://','https://')) else 'https://' + host
    data = {'target': host, 'timestamp': timestamp(), 'findings': [], 'paths': []}
    try:
        r = requests.get(base, timeout=8, allow_redirects=True)
        headers = r.headers
        print(C.GREEN + f"[+] Website reachable: {r.status_code}" + C.RESET)
        for h, meaning in SEC_HEADERS.items():
            if h not in headers:
                data['findings'].append({'id': f'missing_{h.lower().replace("-","_")}', 'title': f'Missing {h}', 'severity': 'Medium' if h in ['Content-Security-Policy','Strict-Transport-Security'] else 'Low', 'status':'Likely', 'confidence':'High', 'impact':meaning, 'fix': f'Add {h} header in server configuration.'})
                print(C.YELLOW + f"[!] Missing header: {h}" + C.RESET)
        cookies = headers.get('Set-Cookie','')
        if cookies and 'HttpOnly' not in cookies:
            data['findings'].append({'id':'cookie_httponly_missing','title':'Cookie missing HttpOnly flag','severity':'Medium','status':'Possible','confidence':'Medium','impact':'JavaScript may access sensitive cookies','fix':'Set HttpOnly flag on session cookies.'})
    except Exception as e:
        data['error'] = str(e)
        print(C.RED + f"[!] Web check failed: {e}" + C.RESET)
        return data, None

    scheme = urlparse(base).scheme
    for p in COMMON_PATHS:
        try:
            rr = requests.get(f'{scheme}://{host}{p}', timeout=4, allow_redirects=False)
            if rr.status_code in [200,301,302,401,403]:
                data['paths'].append({'path':p,'status':rr.status_code})
                sev = 'High' if p in ['/.git/','/backup'] and rr.status_code == 200 else 'Low'
                data['findings'].append({'id':'interesting_path','title':f'Interesting path discovered: {p}','severity':sev,'status':'Possible','confidence':'Medium','impact':'May expose sensitive area or information','fix':'Restrict access and remove exposed files.'})
                print(C.BLUE + f"[i] Path: {p} -> {rr.status_code}" + C.RESET)
        except Exception: pass
    ensure_dirs()
    path = f"{SCAN_DIR}/{safe_filename(host)}_{data['timestamp']}/web_analysis.json"
    save_json(path, data)
    print(C.GREEN + f"[✓] Saved: {path}" + C.RESET)
    return data, path
