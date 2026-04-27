from core.utils import load_json
from core.colors import C

LANGS={'1':('en','English'),'2':('hi','Hindi'),'3':('ml','Malayalam')}
TOPICS={'1':'sql_injection','2':'xss','3':'security_headers','4':'open_ports'}
TYPES={'1':'basic','2':'detailed','3':'example','4':'interview','5':'fix'}

def learning_menu():
    print(C.CYAN+'Learning / Interview Mode'+C.RESET)
    print('[1] English\n[2] Hindi\n[3] Malayalam')
    lang_choice=input('Language: ').strip()
    lang=LANGS.get(lang_choice, LANGS['1'])[0]
    data=load_json(f'data/languages/{lang}_learning.json', {})
    print('\nTopics:\n[1] SQL Injection\n[2] XSS\n[3] Security Headers\n[4] Open Ports')
    topic=TOPICS.get(input('Topic: ').strip(),'sql_injection')
    print('\nType:\n[1] Basic Explanation\n[2] Detailed Technical Explanation\n[3] Real-world Example\n[4] Interview Answer\n[5] Fix & Prevention')
    typ=TYPES.get(input('Type: ').strip(),'basic')
    print(C.GREEN+'\n'+data.get(topic,{}).get(typ,'Content not found.')+C.RESET)
