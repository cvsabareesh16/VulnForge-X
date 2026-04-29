from core.colors import C
from core.utils import timestamp, RESUME_DIR, ensure_dirs
import os, re, html

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


def esc(value):
    return html.escape(str(value or '').strip())


def split_items(value):
    return [item.strip() for item in str(value or '').split(',') if item.strip()]


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
    if not WEASYPRINT_AVAILABLE:
        print(C.YELLOW + '[!] PDF not created. Install WeasyPrint: sudo apt install python3-weasyprint -y' + C.RESET)
        return

    try:
        HTML(filename=html_file).write_pdf(pdf_file)
        print(C.GREEN + f'[+] PDF Resume saved: {pdf_file}' + C.RESET)
    except Exception as e:
        print(C.RED + f'[-] PDF conversion failed: {e}' + C.RESET)


def generate_plain_resume(data, bullets):
    certs_text = data['certs'] if data['certs'] else 'Add relevant cybersecurity certifications or courses here'
    labs_text = data['labs'] if data['labs'] else 'Authorized lab practice and cybersecurity learning projects'

    resume = f"""{data['name'].upper()}
{data['role']}
{data['location']} | {data['email']} | {data['phone']} | {data['github']} | {data['linkedin']}

PROFESSIONAL SUMMARY
{data['summary']}

PROJECTS
"""
    resume += ''.join([f'- {b}\n' for b in bullets])

    resume += f"""
HANDS-ON LABS
- {labs_text}
- Practiced safe scanning, enumeration, service identification, and vulnerability analysis in authorized lab environments.

EDUCATION
{data['education']}

SKILLS
- {data['skills']}
- Cybersecurity Tools: Nmap, Burp Suite, OWASP ZAP, sqlmap basics, Kali Linux
- Core Areas: Reconnaissance, Vulnerability Assessment, Web Security, Risk Analysis, Report Writing

CERTIFICATIONS
{certs_text}

TOOLS
Python, Nmap, Kali Linux, GitHub, Burp Suite, OWASP ZAP, Linux Terminal
"""
    return resume


def generate_html_template(template, data, bullets):
    name = esc(data['name']).upper()
    role = esc(data['role'])
    location = esc(data['location'])
    email = esc(data['email'])
    phone = esc(data['phone'])
    github = esc(data['github'])
    linkedin = esc(data['linkedin'])
    summary = esc(data['summary'])
    education = esc(data['education'])
    certs = split_items(data['certs'])
    skills = split_items(data['skills'])
    labs = esc(data['labs'])
    safe_bullets = [esc(b) for b in bullets]

    if template == '1':
        # Best ATS-friendly template: single column, clean headings, readable text.
        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name} - Resume</title>
<style>
    @page {{ size: A4; margin: 18mm; }}
    body {{
        font-family: Arial, Helvetica, sans-serif;
        color: #000;
        margin: 0;
        font-size: 11.5pt;
        line-height: 1.35;
    }}
    .header {{ text-align: center; margin-bottom: 18px; }}
    h1 {{
        font-size: 30pt;
        margin: 0 0 8px 0;
        letter-spacing: 1.5px;
        font-weight: 800;
    }}
    .role {{
        font-size: 13pt;
        font-weight: 700;
        margin-bottom: 8px;
    }}
    .contact {{ font-size: 10.5pt; }}
    h2 {{
        font-size: 16pt;
        margin: 22px 0 8px 0;
        padding-bottom: 4px;
        border-bottom: 1px solid #222;
        font-weight: 800;
        letter-spacing: .3px;
    }}
    p {{ margin: 6px 0; }}
    ul {{ margin: 6px 0 0 20px; padding: 0; }}
    li {{ margin-bottom: 5px; }}
    .entry-title {{ font-weight: 700; margin-top: 10px; }}
    .small {{ font-size: 10.5pt; }}
</style>
</head>
<body>
    <div class="header">
        <h1>{name}</h1>
        <div class="role">{role}</div>
        <div class="contact">{location} | {email} | {phone} | {github} | {linkedin}</div>
    </div>

    <h2>PROFESSIONAL SUMMARY</h2>
    <p>{summary}</p>

    <h2>PROJECTS</h2>
    <div class="entry-title">VulnForge X — Vulnerability Assessment & Career Toolkit</div>
    <ul>
        {''.join([f'<li>{b}</li>' for b in safe_bullets])}
    </ul>

    <h2>HANDS-ON LABS</h2>
    <ul>
        <li>{labs if labs else 'Authorized cybersecurity practice labs and hands-on learning environments.'}</li>
        <li>Performed safe scanning, enumeration, service identification, documentation, and basic vulnerability analysis.</li>
    </ul>

    <h2>EDUCATION</h2>
    <p>{education}</p>

    <h2>SKILLS</h2>
    <ul>
        {''.join([f'<li>{esc(s)}</li>' for s in skills]) if skills else '<li>Python, Nmap, Kali Linux, Burp Suite, GitHub, Linux</li>'}
    </ul>

    <h2>CERTIFICATIONS</h2>
    <ul>
        {''.join([f'<li>{esc(c)}</li>' for c in certs]) if certs else '<li>Add relevant cybersecurity certifications or courses here</li>'}
    </ul>

    <h2>TOOLS</h2>
    <p>Python, Nmap, Kali Linux, GitHub, Burp Suite, OWASP ZAP, Linux Terminal</p>
</body>
</html>
"""

    elif template == '2':
        # Modern recruiter/HR version with sidebar and optional photo. Not the safest ATS format.
        photo = data.get('photo', '').strip()
        photo_html = f'<img src="file://{esc(os.path.abspath(photo))}" class="photo">' if photo and os.path.exists(photo) else ''
        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name} - Modern Resume</title>
<style>
    @page {{ size: A4; margin: 0; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: #111; }}
    .page {{ display: flex; min-height: 297mm; }}
    .sidebar {{ width: 31%; background: #0f4c3a; color: white; padding: 34px 24px; box-sizing: border-box; }}
    .content {{ width: 69%; padding: 38px 42px; box-sizing: border-box; }}
    .photo {{ width: 92px; height: 92px; border-radius: 50%; object-fit: cover; display: block; margin: 0 auto 18px auto; }}
    .sidebar h1 {{ font-size: 22pt; text-align: center; margin: 8px 0; }}
    .role {{ text-align: center; letter-spacing: 2px; font-size: 9pt; text-transform: uppercase; margin-bottom: 28px; }}
    .sidebar h2 {{ font-size: 15pt; margin-top: 26px; }}
    .sidebar p {{ font-size: 10pt; line-height: 1.45; }}
    .content h2 {{ font-size: 17pt; margin: 0 0 10px 0; }}
    .section {{ margin-bottom: 24px; }}
    li {{ margin-bottom: 6px; }}
</style>
</head>
<body>
<div class="page">
    <div class="sidebar">
        {photo_html}
        <h1>{name.title()}</h1>
        <div class="role">{role}</div>
        <h2>Details</h2>
        <p>{location}<br>{phone}<br>{email}</p>
        <h2>Skills</h2>
        <p>{'<br>'.join([esc(s) for s in skills])}</p>
        <h2>Links</h2>
        <p>{github}<br>{linkedin}</p>
    </div>
    <div class="content">
        <div class="section"><h2>Profile</h2><p>{summary}</p></div>
        <div class="section"><h2>Projects</h2><ul>{''.join([f'<li>{b}</li>' for b in safe_bullets])}</ul></div>
        <div class="section"><h2>Education</h2><p>{education}</p></div>
        <div class="section"><h2>Certifications</h2><p>{', '.join([esc(c) for c in certs]) if certs else 'Add relevant certifications here'}</p></div>
        <div class="section"><h2>Labs</h2><p>{labs}</p></div>
    </div>
</div>
</body>
</html>
"""

    else:
        # Cyber portfolio style.
        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{name} - Cyber Resume</title>
<style>
    @page {{ size: A4; margin: 18mm; }}
    body {{ font-family: Consolas, monospace; background: #080808; color: #00ffcc; }}
    h1 {{ border-bottom: 1px solid #00ffcc; padding-bottom: 8px; }}
    h2 {{ color: #ffffff; margin-top: 24px; }}
    li {{ margin-bottom: 6px; }}
</style>
</head>
<body>
<h1>{name}</h1>
<p>{role} | {email} | {phone} | {github}</p>
<h2>PROFILE</h2><p>{summary}</p>
<h2>SKILLS</h2><p>{', '.join([esc(s) for s in skills])}</p>
<h2>PROJECTS</h2><ul>{''.join([f'<li>{b}</li>' for b in safe_bullets])}</ul>
<h2>LABS</h2><p>{labs}</p>
<h2>EDUCATION</h2><p>{education}</p>
</body>
</html>
"""


def build_resume():
    print(C.CYAN + 'ResumeForge - ATS & Recruiter Ready Resume Builder' + C.RESET)
    print('[1] ATS Resume - Best for job portals')
    print('[2] Modern Resume - HR/Recruiter style with optional photo')
    print('[3] Cybersecurity Portfolio Resume')
    template = input('Select template: ').strip() or '1'

    name = input('Name: ').strip()
    role = input('Target Role (example: Cybersecurity Intern | SOC Analyst Fresher): ').strip() or 'Cybersecurity Learner | Vulnerability Assessment | Python Automation'
    photo = ''
    if template == '2':
        photo = input('Photo path (optional, press Enter to skip): ').strip()

    email = input('Email: ').strip()
    phone = input('Phone: ').strip()
    location = input('Location: ').strip()
    github = input('GitHub URL: ').strip()
    linkedin = input('LinkedIn URL: ').strip()
    education = input('Education: ').strip()
    certs = input('Certifications (comma separated): ').strip()
    skills = input('Skills (comma separated): ').strip()
    labs = input('Labs completed (Metasploitable/VulnHub/TryHackMe etc): ').strip()

    summary = 'Cybersecurity learner with hands-on experience in vulnerability assessment, network scanning, web security analysis, Linux, and Python automation. Strong interest in ethical security testing, documentation, and professional reporting.'

    bullets = [
        'Developed VulnForge X, a CLI-based vulnerability assessment and reporting framework.',
        'Automated reconnaissance, web security checks, risk scoring, and evidence collection using Python.',
        'Generated professional reports in Markdown, HTML, TXT, JSON, and PDF formats.',
        'Built an ATS-friendly resume generator for cybersecurity learners and internship applicants.',
        'Practiced safe lab-based enumeration, scanning, documentation, and vulnerability analysis.'
    ]

    data = {
        'name': name,
        'role': role,
        'photo': photo,
        'email': email,
        'phone': phone,
        'location': location,
        'github': github,
        'linkedin': linkedin,
        'education': education,
        'certs': certs,
        'skills': skills,
        'labs': labs,
        'summary': summary
    }

    resume = generate_plain_resume(data, bullets)
    score, missing = score_resume(resume)

    ensure_dirs()
    safe_name = re.sub(r'[^A-Za-z0-9_-]+', '_', name.strip()) or 'resume'
    base = f'{RESUME_DIR}/{safe_name}_{timestamp()}'

    with open(base + '.txt', 'w', encoding='utf-8') as f:
        f.write(resume)

    with open(base + '.md', 'w', encoding='utf-8') as f:
        f.write('# ' + resume.replace('\n', '\n'))

    html_content = generate_html_template(template, data, bullets)
    with open(base + '.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    convert_html_to_pdf(base + '.html', base + '.pdf')

    print(C.GREEN + f'\nATS Optimization Estimate: {score}/100' + C.RESET)
    if missing:
        print(C.YELLOW + 'Suggested keywords to add if truthful: ' + ', '.join(missing) + C.RESET)

    print(C.GREEN + f'Saved: {base}.txt / .md / .html / .pdf' + C.RESET)
