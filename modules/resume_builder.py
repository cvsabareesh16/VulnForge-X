from core.colors import C
from core.utils import timestamp, RESUME_DIR, ensure_dirs
import os
import re
import html as html_escape

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except Exception:
    HTML = None
    WEASYPRINT_AVAILABLE = False


KEYWORDS = [
    'Python', 'Nmap', 'Kali Linux', 'Vulnerability Assessment', 'Web Security',
    'Risk Analysis', 'Security Reporting', 'Burp Suite', 'OWASP ZAP', 'Linux',
    'GitHub', 'Reconnaissance'
]


def score_resume(text):
    score = 50
    found = []

    for k in KEYWORDS:
        if k.lower() in text.lower():
            score += 3
            found.append(k)

    sections = ['SUMMARY', 'SKILLS', 'PROJECTS', 'EDUCATION', 'CERTIFICATIONS', 'TOOLS']
    for s in sections:
        if s in text.upper():
            score += 3

    score = min(95, score)
    missing = [k for k in KEYWORDS if k not in found][:6]
    return score, missing


def convert_html_to_pdf(html_file, pdf_file):
    """Convert generated HTML resume to PDF using WeasyPrint."""
    if not WEASYPRINT_AVAILABLE:
        print(C.YELLOW + '[!] PDF skipped: WeasyPrint is not installed.' + C.RESET)
        print(C.YELLOW + 'Install it with: sudo apt install python3-weasyprint -y' + C.RESET)
        return False

    try:
        HTML(filename=html_file).write_pdf(pdf_file)
        print(C.GREEN + f'[+] PDF Resume saved: {pdf_file}' + C.RESET)
        return True
    except Exception as e:
        print(C.RED + f'[-] PDF conversion failed: {e}' + C.RESET)
        return False


def safe(value):
    """Escape user input before putting it inside HTML."""
    return html_escape.escape(str(value or ''))


def list_items(items):
    return ''.join(f'<li>{safe(item)}</li>' for item in items if str(item).strip())


def split_csv(value):
    return [x.strip() for x in str(value or '').split(',') if x.strip()]


def generate_html_template(template, data):
    name = safe(data['name'])
    email = safe(data['email'])
    phone = safe(data['phone'])
    location = safe(data['location'])
    github = safe(data['github'])
    linkedin = safe(data['linkedin'])
    summary = safe(data['summary'])
    education = safe(data['education'])
    certs = safe(data['certs']) if data['certs'] else 'Add relevant cybersecurity certifications or courses here'
    labs = safe(data['labs']) if data['labs'] else 'Authorized practice labs and hands-on cybersecurity learning.'
    skill_items = list_items(split_csv(data['skills']))
    bullet_items = list_items(data['bullets'])

    # 1 = ATS Clean: simple, single-column, job portal friendly
    if template == '1':
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name} - ATS Resume</title>
<style>
    body {{ font-family: Arial, sans-serif; color: #111; line-height: 1.45; margin: 36px; }}
    h1 {{ font-size: 26px; margin-bottom: 4px; }}
    h2 {{ font-size: 16px; margin-top: 22px; border-bottom: 1px solid #222; padding-bottom: 4px; }}
    p {{ margin: 6px 0; }}
    ul {{ margin-top: 6px; }}
    li {{ margin-bottom: 5px; }}
    .contact {{ font-size: 12px; }}
</style>
</head>
<body>
    <h1>{name}</h1>
    <p class="contact">{email} | {phone} | {location}</p>
    <p class="contact">GitHub: {github} | LinkedIn: {linkedin}</p>

    <h2>SUMMARY</h2>
    <p>{summary}</p>

    <h2>SKILLS</h2>
    <ul>{skill_items}</ul>
    <p><strong>Cybersecurity Tools:</strong> Nmap, Burp Suite, OWASP ZAP, sqlmap basics, Kali Linux</p>
    <p><strong>Core Areas:</strong> Reconnaissance, Vulnerability Assessment, Web Security, Risk Analysis, Report Writing</p>

    <h2>PROJECTS</h2>
    <p><strong>VulnForge X — Vulnerability Assessment & Career Toolkit</strong></p>
    <ul>{bullet_items}</ul>

    <h2>HANDS-ON LABS</h2>
    <p>{labs}</p>

    <h2>EDUCATION</h2>
    <p>{education}</p>

    <h2>CERTIFICATIONS</h2>
    <p>{certs}</p>

    <h2>TOOLS</h2>
    <p>Python, Nmap, Kali Linux, GitHub, Burp Suite, OWASP ZAP, Linux Terminal</p>
</body>
</html>'''

    # 2 = Modern Professional: clean recruiter-friendly visual template
    if template == '2':
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name} - Modern Resume</title>
<style>
    body {{ font-family: Arial, sans-serif; background: #f4f6f8; color: #1f2937; margin: 0; padding: 28px; }}
    .page {{ background: #fff; padding: 34px; border-radius: 14px; max-width: 820px; margin: auto; }}
    h1 {{ margin: 0; font-size: 30px; color: #111827; }}
    .role {{ margin-top: 6px; font-size: 15px; color: #374151; }}
    .contact {{ margin-top: 8px; font-size: 12px; color: #4b5563; }}
    h2 {{ margin-top: 26px; font-size: 16px; color: #0f766e; text-transform: uppercase; letter-spacing: .6px; }}
    p {{ line-height: 1.5; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 6px; }}
    .tag {{ display: inline-block; border: 1px solid #d1d5db; padding: 4px 8px; border-radius: 14px; margin: 3px; font-size: 12px; }}
</style>
</head>
<body>
<div class="page">
    <h1>{name}</h1>
    <div class="role">Cybersecurity Learner | Vulnerability Assessment | Python Automation</div>
    <div class="contact">{email} | {phone} | {location}</div>
    <div class="contact">GitHub: {github} | LinkedIn: {linkedin}</div>

    <h2>Professional Summary</h2>
    <p>{summary}</p>

    <h2>Core Skills</h2>
    <div>{''.join(f'<span class="tag">{safe(s)}</span>' for s in split_csv(data['skills']))}</div>

    <h2>Featured Project</h2>
    <p><strong>VulnForge X — Vulnerability Assessment & Career Toolkit</strong></p>
    <ul>{bullet_items}</ul>

    <h2>Hands-on Labs</h2>
    <p>{labs}</p>

    <h2>Education</h2>
    <p>{education}</p>

    <h2>Certifications</h2>
    <p>{certs}</p>
</div>
</body>
</html>'''

    # 3 = Cybersecurity Portfolio: stylish for GitHub/LinkedIn sharing
    if template == '3':
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name} - Cybersecurity Resume</title>
<style>
    body {{ font-family: 'Courier New', monospace; background: #0b1020; color: #d1fae5; margin: 0; padding: 30px; }}
    .page {{ max-width: 860px; margin: auto; border: 1px solid #10b981; padding: 30px; border-radius: 12px; background: #111827; }}
    h1 {{ color: #34d399; margin-bottom: 5px; }}
    h2 {{ color: #5eead4; border-bottom: 1px solid #134e4a; padding-bottom: 5px; margin-top: 24px; }}
    p, li {{ line-height: 1.5; }}
    .contact {{ color: #a7f3d0; font-size: 13px; }}
    .hint {{ color: #93c5fd; }}
</style>
</head>
<body>
<div class="page">
    <h1>{name}</h1>
    <p class="contact">{email} | {phone} | {location}</p>
    <p class="contact">GitHub: {github} | LinkedIn: {linkedin}</p>

    <h2>&gt; Cybersecurity Profile</h2>
    <p>{summary}</p>

    <h2>&gt; Skills</h2>
    <ul>{skill_items}</ul>

    <h2>&gt; Project</h2>
    <p class="hint">VulnForge X — Vulnerability Assessment & Career Toolkit</p>
    <ul>{bullet_items}</ul>

    <h2>&gt; Labs</h2>
    <p>{labs}</p>

    <h2>&gt; Education</h2>
    <p>{education}</p>

    <h2>&gt; Certifications</h2>
    <p>{certs}</p>
</div>
</body>
</html>'''

    # fallback
    return generate_html_template('1', data)


def build_resume():
    print(C.CYAN + 'ResumeForge - 2026 ATS & Recruiter Ready Resume Builder' + C.RESET)
    print('\nChoose Template:')
    print('[1] ATS Clean Resume - best for Naukri, LinkedIn Easy Apply, job portals')
    print('[2] Modern Professional Resume - best for HR email and recruiter sharing')
    print('[3] Cybersecurity Portfolio Resume - best for GitHub/LinkedIn portfolio')

    template = input('Select template: ').strip() or '1'
    if template not in ['1', '2', '3']:
        print(C.YELLOW + '[!] Invalid template selected. Using ATS Clean Resume.' + C.RESET)
        template = '1'

    name = input('Name: ').strip()
    email = input('Email: ').strip()
    phone = input('Phone: ').strip()
    location = input('Location: ').strip()
    github = input('GitHub URL: ').strip()
    linkedin = input('LinkedIn URL: ').strip()
    education = input('Education: ').strip()
    certs = input('Certifications (comma separated): ').strip()
    skills = input('Skills (comma separated): ').strip()
    labs = input('Labs completed (Metasploitable/VulnHub etc): ').strip()

    if not name:
        name = 'Your Name'

    summary = (
        'Cybersecurity learner with hands-on experience in vulnerability assessment, '
        'network scanning, web security analysis, Linux, and Python automation. Strong '
        'interest in ethical security testing, documentation, and professional reporting.'
    )

    bullets = [
        'Developed VulnForge X, a CLI-based vulnerability assessment and reporting framework.',
        'Automated reconnaissance, web security checks, risk scoring, and evidence collection using Python.',
        'Implemented multilingual learning and interview preparation support in English, Hindi, and Malayalam.',
        'Generated professional reports in Markdown, HTML, TXT, JSON, and PDF formats.',
        'Designed an ATS-friendly resume generator for cybersecurity learners and internship applicants.'
    ]

    resume = f"""{name.upper()}
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
        resume += (
            f"\nHANDS-ON LABS\n"
            f"- Completed practice labs: {labs}\n"
            f"- Performed safe scanning, enumeration, service identification, and vulnerability analysis in authorized lab environments.\n"
        )

    resume += f"""
EDUCATION
{education}

CERTIFICATIONS
{certs if certs else 'Add relevant cybersecurity certifications or courses here'}

TOOLS
Python, Nmap, Kali Linux, GitHub, Burp Suite, OWASP ZAP, Linux Terminal
"""

    score, missing = score_resume(resume)
    ensure_dirs()

    safe_name = re.sub(r'[^A-Za-z0-9_-]+', '_', name.strip()).strip('_') or 'resume'
    base = f'{RESUME_DIR}/{safe_name}_{timestamp()}'

    txt_file = base + '.txt'
    md_file = base + '.md'
    html_file = base + '.html'
    pdf_file = base + '.pdf'

    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(resume)

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('# ' + resume.replace('\n', '\n'))

    data = {
        'name': name,
        'email': email,
        'phone': phone,
        'location': location,
        'github': github,
        'linkedin': linkedin,
        'summary': summary,
        'skills': skills,
        'education': education,
        'certs': certs,
        'bullets': bullets,
        'labs': labs
    }

    html = generate_html_template(template, data)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    convert_html_to_pdf(html_file, pdf_file)

    print(C.GREEN + f'\nATS Optimization Estimate: {score}/100' + C.RESET)
    if missing:
        print(C.YELLOW + 'Suggested keywords to add if truthful: ' + ', '.join(missing) + C.RESET)

    print(C.GREEN + f'Saved: {txt_file} / {md_file} / {html_file}' + C.RESET)
    if os.path.exists(pdf_file):
        print(C.GREEN + f'PDF Ready: {pdf_file}' + C.RESET)

