from core.colors import C

GUIDES = {
 'sql_injection': ['Identify parameters and forms only on authorized target.','Use Burp Suite/OWASP ZAP to observe request and response behavior.','Look for database error messages or unexpected response changes.','Confirm in a lab or permitted scope before reporting.','Fix: prepared statements, ORM parameterization, input validation.'],
 'xss': ['Identify reflected input points such as search fields or query parameters.','Use safe non-destructive reflection checks in an authorized lab.','Check if output is encoded correctly.','Fix: output encoding, Content-Security-Policy, input validation.'],
 'headers': ['Review missing security headers.','Confirm whether reverse proxy or application should set them.','Fix server configuration and retest.'],
 'service': ['Check exact service version.','Search vendor advisories and CVEs.','Restrict service exposure and patch.']
}

def validation_menu():
    print(C.CYAN+'Validation Assistant (safe/manual only)'+C.RESET)
    print('[1] SQL Injection validation checklist')
    print('[2] XSS validation checklist')
    print('[3] Security headers validation checklist')
    print('[4] Service/CVE validation checklist')
    choice=input('Select: ').strip()
    key={'1':'sql_injection','2':'xss','3':'headers','4':'service'}.get(choice)
    if not key: return
    print(C.YELLOW+'\nOnly test systems you own or have written permission to test.\n'+C.RESET)
    for i, step in enumerate(GUIDES[key],1):
        print(f'{C.GREEN}{i}.{C.RESET} {step}')
