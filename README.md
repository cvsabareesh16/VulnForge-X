# VulnForge X
### Vulnerability Assessment & Career Toolkit for Ethical Security Testing

VulnForge X is a Python-based colorful CLI framework built for cybersecurity learners, interns, and junior security candidates. It combines safe reconnaissance, vulnerability analysis, risk scoring, reporting, multilingual learning, interview preparation, and ATS resume generation.

> **Legal Notice:** Use only on systems you own or have explicit written permission to test. VulnForge X does not auto-exploit targets.

## Features

- Colorful Kali-style terminal interface
- Reconnaissance and scanning workflow
- Nmap integration if installed
- Web security header analysis
- Safe directory/path discovery
- Subdomain discovery
- Vulnerability risk engine
- Safe exploitation/validation assistant
- Risk score dashboard
- Professional report generation: Markdown, TXT, HTML
- Evidence and logs manager
- Multilingual learning and interview mode:
  - English
  - Hindi
  - Malayalam
- ResumeForge ATS resume builder:
  - ATS resume
  - Cybersecurity resume
  - Internship/fresher resume
  - Project-focused resume
  - Minimal one-page resume

## Main Menu

```text
[1] Reconnaissance & Scanning
[2] Enumeration & Vulnerability Analysis
[3] Exploitation / Validation Assistant (Safe)
[4] Risk Score Dashboard
[5] Generate Professional Report
[6] Evidence & Logs
[7] Learning / Interview Mode (EN/HI/ML)
[8] ResumeForge - ATS Resume Builder
[9] Run Full Auto Assessment
[10] Settings / Help
[0] Exit
```

## Installation on Kali Linux

```bash
git clone https://github.com/yourname/VulnForge-X.git
cd VulnForge-X
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt install nmap -y
python3 main.py
```

## Why This Project Is Useful

This project demonstrates:

- Python automation
- Network reconnaissance
- Web security basics
- Vulnerability assessment thinking
- Risk scoring
- Security report writing
- Multilingual explanation system
- Resume-building support for job seekers

## Safe Design

VulnForge X is designed as an assessment and reporting framework. It does not brute-force, auto-exploit, or run destructive tests. The Validation Assistant provides safe manual checklists for authorized testing and lab practice.

## ResumeForge

ResumeForge helps generate clean ATS-friendly resumes with cybersecurity keywords and project-focused bullet points. It does not guarantee a 100/100 ATS score because ATS systems differ, but it helps improve structure, keywords, and readability.

## Suggested GitHub Screenshots

Add screenshots of:

1. Main menu
2. Recon scan result
3. Risk dashboard
4. Learning mode in Malayalam/Hindi/English
5. Generated report
6. ResumeForge output

## Project Structure

```text
VulnForge-X/
├── main.py
├── core/
├── modules/
├── reports/
├── data/
├── results/
│   ├── scans/
│   ├── reports/
│   ├── resumes/
│   ├── logs/
│   └── evidence/
├── docs/
├── samples/
├── requirements.txt
├── instruction.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Disclaimer

This tool is for education, portfolio building, and authorized security assessment only. The author is not responsible for misuse.

## Results Folder Structure

All generated files are stored in one clean `results/` folder:

```text
results/
├── scans/      # Recon, Nmap, web analysis, subdomain, vulnerability JSON outputs
├── reports/    # Security assessment reports in MD, TXT, and HTML
├── resumes/    # ATS and recruiter-ready resume outputs
├── logs/       # Runtime or future scan logs
└── evidence/   # Manual proof files/screenshots can be added here
```

This makes the project easier to review on GitHub and easier to explain in interviews.
