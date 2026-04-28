#!/usr/bin/env python3

from core.banner import show_banner
from core.menu import main_menu
from core.utils import ensure_dirs
from modules.recon_scanner import run_recon
from modules.web_analyzer import analyze_web
from modules.vuln_analyzer import analyze_findings
from modules.validation_assistant import validation_menu
from modules.risk_engine import show_dashboard
from modules.subdomain_scanner import scan_subdomains
from modules.evidence_manager import list_evidence
from modules.learning_mode import learning_menu
from modules.resume_builder import build_resume
from reports.report_generator import generate_report
from core.colors import C


state = {
    'target': None,
    'recon': None,
    'web': None,
    'analysis': None
}


def get_target():
    target = input("\nEnter target (IP / URL): ").strip()

    if not target:
        print(C.RED + "Target cannot be empty." + C.RESET)
        return None

    return target


def legal_prompt():
    print(C.YELLOW + 'This tool is for ethical testing only. Use it only on systems you own or have permission to test.' + C.RESET)
    ans = input('Type I AGREE to continue: ').strip()
    return ans == 'I AGREE'


def auto_assessment():
    target = get_target()

    if not target:
        return

    state['target'] = target
    state['recon'], _ = run_recon(target)
    state['web'], _ = analyze_web(target)

    try:
        scan_subdomains(target)
    except Exception:
        pass

    state['analysis'], _ = analyze_findings(target, state['recon'], state['web'])
    generate_report(target, state['analysis'], state['recon'], state['web'])


def main():
    ensure_dirs()
    show_banner()

    if not legal_prompt():
        print(C.RED + 'Authorization not confirmed. Exiting.' + C.RESET)
        return

    while True:
        choice = main_menu()

        if choice == '1':
            target = get_target()
            if target:
                state['target'] = target
                state['recon'], _ = run_recon(target)

        elif choice == '2':
            target = get_target()
            if target:
                state['target'] = target
                state['analysis'], _ = analyze_findings(target, state['recon'], state['web'])

        elif choice == '3':
            validation_menu()

        elif choice == '4':
            show_dashboard(state['analysis'])

        elif choice == '5':
            target = get_target()
            if target:
                state['target'] = target
                generate_report(target, state['analysis'], state['recon'], state['web'])

        elif choice == '6':
            list_evidence()

        elif choice == '7':
            learning_menu()

        elif choice == '8':
            build_resume()

        elif choice == '9':
            auto_assessment()

        elif choice == '10':
            print(C.CYAN + 'Help:' + C.RESET)
            print('1) Use only authorized targets.')
            print('2) Run Auto Assessment for full workflow.')
            print('3) Use Report and Resume modules for portfolio.')

        elif choice == '0':
            print(C.GREEN + 'Goodbye. Stay ethical!' + C.RESET)
            break

        else:
            print(C.RED + 'Invalid option.' + C.RESET)

        input('\nPress Enter to continue...')


if __name__ == '__main__':
    main()
