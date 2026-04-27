from core.colors import C
from core.utils import save_json, timestamp, safe_filename, normalize_target, SCAN_DIR, ensure_dirs

RISKY_SERVICES = {
    'ftp': ('Medium','FTP may expose credentials if not protected.'),
    'telnet': ('High','Telnet sends data in clear text.'),
    'smb': ('High','SMB exposure can increase lateral movement risk.'),
    'mysql': ('Medium','Database service should not be public unless required.'),
    'rdp': ('High','RDP exposed to untrusted networks is high risk.'),
    'apache': ('Low','Check exact version and patch status.'),
    'openssh': ('Low','Keep OpenSSH updated and disable password login if possible.')
}

def analyze_findings(target, recon=None, web=None):
    host = normalize_target(target)
    findings = []
    if web and web.get('findings'):
        findings.extend(web['findings'])
    if recon:
        for line in recon.get('open_ports', []):
            l = line.lower()
            for key, (sev, impact) in RISKY_SERVICES.items():
                if key in l:
                    findings.append({'id':f'service_{key}','title':f'Potential risky service: {key.upper()}','severity':sev,'status':'Possible','confidence':'Medium','impact':impact,'fix':'Verify business need, restrict access, and patch to latest secure version.','evidence':line})
    if not findings:
        findings.append({'id':'no_major_findings','title':'No obvious issues detected','severity':'Info','status':'Not Detected','confidence':'Low','impact':'Automated checks did not identify clear issues. Manual testing is still recommended.','fix':'Run deeper authorized testing and review configuration.'})
    score = calculate_score(findings)
    data = {'target':host,'timestamp':timestamp(),'score':score,'findings':findings}
    ensure_dirs()
    path = f"{SCAN_DIR}/{safe_filename(host)}_{data['timestamp']}/vulnerability_analysis.json"
    save_json(path, data)
    print(C.GREEN + f"[✓] Risk Score: {score['score']}/100 ({score['level']})" + C.RESET)
    return data, path

def calculate_score(findings):
    penalty = 0
    weights = {'Critical':30,'High':20,'Medium':10,'Low':4,'Info':0}
    counts = {'Critical':0,'High':0,'Medium':0,'Low':0,'Info':0}
    for f in findings:
        sev = f.get('severity','Info')
        counts[sev] = counts.get(sev,0)+1
        penalty += weights.get(sev,0)
    score = max(0, 100 - penalty)
    level = 'Low Risk' if score >= 80 else 'Moderate Risk' if score >= 60 else 'High Risk' if score >= 35 else 'Critical Risk'
    return {'score':score,'level':level,'counts':counts}
