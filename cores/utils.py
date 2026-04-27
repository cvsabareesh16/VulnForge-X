import json, os, socket, re
from datetime import datetime
from urllib.parse import urlparse

RESULTS_DIR='results'
SCAN_DIR=os.path.join(RESULTS_DIR, 'scans')
REPORT_DIR=os.path.join(RESULTS_DIR, 'reports')
RESUME_DIR=os.path.join(RESULTS_DIR, 'resumes')
LOG_DIR=os.path.join(RESULTS_DIR, 'logs')
EVIDENCE_DIR=os.path.join(RESULTS_DIR, 'evidence')

def ensure_dirs():
    for d in [RESULTS_DIR, SCAN_DIR, REPORT_DIR, RESUME_DIR, LOG_DIR, EVIDENCE_DIR]:
        os.makedirs(d, exist_ok=True)

def timestamp():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def normalize_target(target):
    target = target.strip()
    if not target:
        return ''
    parsed = urlparse(target if '://' in target else 'http://' + target)
    return parsed.netloc or parsed.path

def resolve_ip(host):
    try:
        return socket.gethostbyname(host)
    except Exception:
        return 'Not resolved'

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path, default=None):
    try:
        with open(path, encoding='utf-8') as f: return json.load(f)
    except Exception: return default if default is not None else {}

def safe_filename(s):
    return re.sub(r'[^A-Za-z0-9_.-]+','_',s)[:80]
