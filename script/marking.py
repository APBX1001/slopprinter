from IPython.core.magic import register_line_magic
from IPython import get_ipython
from pathlib import Path
from nenen88 import tempe
import json
import os

SM = None

try:
    from KANDANG import TEMPPATH, HOMEPATH
    TMP = Path(TEMPPATH)
    HOME = Path(HOMEPATH)
    SM = False
except ImportError:
    TMP = Path('/tmp')
    HOME = Path.home()
    SM = True

marked = Path(__file__).parent / 'marking.json'

SyS = get_ipython().system
CD = os.chdir

def purgeVAR():
    l = [
        'WebUI', 'Models', 'WebUI_Output', 'Extensions', 'Embeddings', 'VAE',
        'CKPT', 'LORA', 'TMP_CKPT', 'TMP_LORA', 'Controlnet_Widget', 'Upscalers'
    ]
    for v in l:
        if v in globals(): del globals()[v]

def getWebUIName(path):
    return json.load(open(path, 'r')).get('ui', None)

def setWebUIVAR(ui):
    # Fallback if the UI isn't one of the two supported
    if ui not in ['Forge-Classic', 'Forge-Neo']:
        return (None,) * 9
        
    ext, embed, vae, ckpt, lora, upscaler = ('extensions', 'embeddings', 'VAE', 'Stable-diffusion', 'Lora', 'ESRGAN')

    WebUI = HOME / ui
    Models = WebUI / 'models'
    WebUI_Output = WebUI / 'output'
    Extensions = WebUI / ext 
    Embeddings = Models / embed
    VAE = Models / vae
    CKPT = Models / ckpt
    LORA = Models / lora
    Upscalers = Models / upscaler

    return WebUI, Models, WebUI_Output, Extensions, Embeddings, VAE, CKPT, LORA, Upscalers

if SM:
    @register_line_magic
    def clear_output_images(line):
        ui = getWebUIName(marked)
        _, _, output, _, _, _, _, _, _ = setWebUIVAR(ui)
        if output:
            SyS(f"rm -rf {output}/* {HOME / '.cache/*'}")
        CD(HOME)
        print(f'{ui} outputs cleared.')

    @register_line_magic
    def uninstall_webui(line):
        ui = getWebUIName(marked)
        webui, _, _, _, _, _, _, _, _ = setWebUIVAR(ui)
        if webui:
            SyS(f"rm -rf {webui} {HOME / 'tmp'} {HOME / '.cache/*'}")
        print(f'{ui} uninstalled.')
        CD(HOME)
        get_ipython().kernel.do_shutdown(True)

if marked.exists():
    purgeVAR()

    ui = getWebUIName(marked)
    WebUI, Models, WebUI_Output, Extensions, Embeddings, VAE, CKPT, LORA, Upscalers = setWebUIVAR(ui)

    Controlnet_Widget = WebUI / 'asd/controlnet.py' if WebUI else None
    TMP_CKPT = TMP / 'ckpt'
    TMP_LORA = TMP / 'lora'

    tempe()
