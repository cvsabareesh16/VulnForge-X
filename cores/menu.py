from core.colors import C

def main_menu():
    print(C.BOLD + C.WHITE + "Main Menu" + C.RESET)
    items = [
        'Reconnaissance & Scanning',
        'Enumeration & Vulnerability Analysis',
        'Exploitation / Validation Assistant (Safe)',
        'Risk Score Dashboard',
        'Generate Professional Report',
        'Evidence & Logs',
        'Learning / Interview Mode (EN/HI/ML)',
        'ResumeForge - ATS Resume Builder',
        'Run Full Auto Assessment',
        'Settings / Help'
    ]
    for i, item in enumerate(items, 1):
        print(f"{C.CYAN}[{i}]{C.RESET} {item}")
    print(f"{C.RED}[0]{C.RESET} Exit")
    return input('\nSelect option: ').strip()
