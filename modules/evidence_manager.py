import os, glob
from core.colors import C
from core.utils import RESULTS_DIR, ensure_dirs

def list_evidence():
    ensure_dirs()
    dirs = sorted(glob.glob(RESULTS_DIR+'/*'), reverse=True)
    if not dirs:
        print(C.YELLOW+'No results folders yet.'+C.RESET); return
    for d in dirs[:10]:
        print(C.CYAN+d+C.RESET)
        for f in glob.glob(d+'/*'):
            print('  - '+os.path.basename(f))
