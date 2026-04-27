from core.colors import C
from core.utils import timestamp, RESUME_DIR, ensure_dirs
import os, re

KEYWORDS = ['Python','Nmap','Kali Linux','Vulnerability Assessment','Web Security','Risk Analysis','Security Reporting','Burp Suite','OWASP ZAP','Linux','GitHub','Reconnaissance']

def score_resume(text):
    score=50
    found=[]
    for k in KEYWORDS:
        if k.lower() in text.lower():
            score+=3; found.append(k)
    sections=['SUMMARY','SKILLS','PROJECTS','EDUCATION','CERTIFICATIONS','TOOLS']
    for s in sections:
        if s in text.upper(): score+=3
    score=min(95, score)
    missing=[k for k in KEYWORDS if k not in found][:6]
    return score, missing

def build_resume():
    print(C.CYAN+'ResumeForge - ATS & Recruiter Ready Resume Builder'+C.RESET)
    print('[1] ATS Resume\n[2] Cybersecurity Resume\n[3] Internship/Fresher Resume\n[4] Project-Focused Resume\n[5] Minimal One-Page Resume')
    rtype=input('Select resume type: ').strip() or '4'
    name=input('Name: ').strip()
    email=input('Email: ').strip()
    phone=input('Phone: ').strip()
    location=input('Location: ').strip()
    github=input('GitHub URL: ').strip()
    linkedin=input('LinkedIn URL: ').strip()
    education=input('Education: ').strip()
    certs=input('Certifications (comma separated): ').strip()
    skills=input('Skills (comma separated): ').strip()
    labs=input('Labs completed (Metasploitable/VulnHub etc): ').strip()

    summary='Cybersecurity learner with hands-on experience in vulnerability assessment, network scanning, web security analysis, Linux, and Python automation. Strong interest in ethical security testing, documentation, and professional reporting.'
    bullets=[
        'Developed VulnForge X, a CLI-based vulnerability assessment and reporting framework.',
        'Automated reconnaissance, web security checks, risk scoring, and evidence collection using Python.',
        'Implemented multilingual learning and interview preparation support in English, Hindi, and Malayalam.',
        'Generated professional reports in Markdown, HTML, TXT, and JSON formats.',
        'Designed an ATS-friendly resume generator for cybersecurity learners and internship applicants.'
    ]
    resume=f"""{name.upper()}
Email: {email} | Phone: {phone} | Location: {location}
GitHub: {github} | LinkedIn: {linkedin}

SUMMARY
{summary}

SKILLS
- {skills}
- Cybersecurity Tools: Nmap, Burp Suite, OWASP ZAP, sqlmap basics, Kali Linux
- Core Areas: Reconnaissance, Vulnerability Assessment, Web Security, Risk Analysis, Report Writing

PROJECTS
VulnForge X — Vulnerability Assessment & Career Toolkit
"""
    resume += ''.join([f'- {b}\n' for b in bullets])
    if labs:
        resume += f"\nHANDS-ON LABS\n- Completed practice labs: {labs}\n- Performed safe scanning, enumeration, service identification, and vulnerability analysis in authorized lab environments.\n"
    resume += f"""
EDUCATION
{education}

CERTIFICATIONS
{certs if certs else 'Add relevant cybersecurity certifications or courses here'}

TOOLS
Python, Nmap, Kali Linux, GitHub, Burp Suite, OWASP ZAP, Linux Terminal
"""
    score, missing=score_resume(resume)
    ensure_dirs()
    base=f'{RESUME_DIR}/{name.replace(" ","_")}_{timestamp()}'
    open(base+'.txt','w',encoding='utf-8').write(resume)
    open(base+'.md','w',encoding='utf-8').write('# '+resume.replace('\n','\n'))
    html='<html><body><pre style="font-family:Arial;white-space:pre-wrap">'+resume+'</pre></body></html>'
    open(base+'.html','w',encoding='utf-8').write(html)
    print(C.GREEN+f'\nATS Optimization Estimate: {score}/100'+C.RESET)
    if missing:
        print(C.YELLOW+'Suggested keywords to add if truthful: '+', '.join(missing)+C.RESET)
    print(C.GREEN+f'Saved: {base}.txt / .md / .html'+C.RESET)
