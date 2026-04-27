import requests
from core.utils import normalize_target, save_json, timestamp, safe_filename, SCAN_DIR, ensure_dirs
from core.colors import C

def scan_subdomains(target, wordlist='data/subdomains.txt'):
    host = normalize_target(target).replace('www.','')
    found=[]
    try:
        words=[w.strip() for w in open(wordlist) if w.strip()]
    except Exception: words=['www','mail','dev','test','admin','api']
    for w in words:
        sub=f'{w}.{host}'
        try:
            r=requests.get('https://'+sub,timeout=3)
            found.append({'subdomain':sub,'status':r.status_code})
            print(C.GREEN+f'[+] Live: {sub} ({r.status_code})'+C.RESET)
        except Exception: pass
    data={'target':host,'timestamp':timestamp(),'subdomains':found}
    ensure_dirs()
    path=f"{SCAN_DIR}/{safe_filename(host)}_{data['timestamp']}/subdomains.json"
    save_json(path,data)
    return data,path
