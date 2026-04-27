from core.colors import C

def show_banner():
    print(C.CYAN + r'''
╔════════════════════════════════════════════════════════════╗
║                     VulnForge X                           ║
║     Vulnerability Assessment & Career Toolkit              ║
║        Recon | Analyze | Validate | Report | Resume        ║
╚════════════════════════════════════════════════════════════╝
''' + C.RESET)
    print(C.YELLOW + "Safe Mode: ON | Use only on systems you own or have permission to test\n" + C.RESET)
