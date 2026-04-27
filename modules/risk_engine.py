from core.colors import C

def show_dashboard(analysis):
    if not analysis:
        print(C.YELLOW+'Run vulnerability analysis first.'+C.RESET); return
    score = analysis.get('score', {})
    print(C.CYAN+'\nRisk Score Dashboard'+C.RESET)
    print(f"Overall Score: {score.get('score','N/A')}/100")
    print(f"Risk Level: {score.get('level','N/A')}")
    print('Findings:')
    for k,v in score.get('counts',{}).items(): print(f'  {k}: {v}')
    print('\nTop Findings:')
    for f in analysis.get('findings',[])[:5]: print(f"- [{f.get('severity')}] {f.get('title')}")
