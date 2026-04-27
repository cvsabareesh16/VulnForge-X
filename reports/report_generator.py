import os, json
from core.utils import timestamp, safe_filename, normalize_target, REPORT_DIR, ensure_dirs
from core.colors import C

def generate_report(target, analysis=None, recon=None, web=None):
    host=normalize_target(target)
    ensure_dirs()
    if not analysis: analysis={'score':{'score':'N/A','level':'N/A','counts':{}},'findings':[]}
    lines=[]
    lines.append(f'# VulnForge X Security Assessment Report\n')
    lines.append(f'**Target:** {host}  \n**Date:** {timestamp()}  \n**Safe Mode:** Enabled\n')
    lines.append('## Executive Summary\nThis report summarizes safe automated reconnaissance and vulnerability assessment indicators. Findings require manual validation before being treated as confirmed vulnerabilities.\n')
    lines.append(f"## Overall Risk Score\nScore: **{analysis.get('score',{}).get('score')} / 100**  \nRisk Level: **{analysis.get('score',{}).get('level')}**\n")
    lines.append('## Findings\n')
    if analysis.get('findings'):
        for f in analysis['findings']:
            lines.append(f"### [{f.get('severity')}] {f.get('title')}\n- Status: {f.get('status')}\n- Confidence: {f.get('confidence')}\n- Impact: {f.get('impact')}\n- Recommendation: {f.get('fix')}\n")
    else:
        lines.append('No findings recorded.\n')
    lines.append('## Methodology\n- Reconnaissance and scanning\n- Web configuration analysis\n- Service risk mapping\n- Risk scoring\n- Report generation\n')
    lines.append('## Legal Note\nUse only on systems you own or have explicit written permission to test.\n')
    md='\n'.join(lines)
    base=f"{REPORT_DIR}/{safe_filename(host)}_{timestamp()}"
    open(base+'.md','w',encoding='utf-8').write(md)
    open(base+'.txt','w',encoding='utf-8').write(md.replace('#',''))
    html='<html><head><title>VulnForge X Report</title><style>body{font-family:Arial;margin:40px} h1,h2{color:#0b7285} .sev{font-weight:bold}</style></head><body>'+md.replace('\n','<br>').replace('# ','<h1>').replace('## ','<h2>').replace('### ','<h3>')+'</body></html>'
    open(base+'.html','w',encoding='utf-8').write(html)
    print(C.GREEN+f'[✓] Reports saved: {base}.md / .txt / .html'+C.RESET)
    return base
