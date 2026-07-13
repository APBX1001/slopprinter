from IPython.core.magic import register_line_magic
from IPython import get_ipython
from pathlib import Path
import json
import os

from _segsmaker_ import HOME, SRC
from nenen88 import tempe

CD = os.chdir
iRON = os.environ
SyS = get_ipython().system

TMP = Path('/tmp')
MARK = SRC / 'marking.json'

ui = json.load(MARK.open()).get('ui')

SSL = 'SAGEMAKER_INTERNAL_IMAGE_URI' in iRON

def _del():
    l = [
        'WebUI', 'Models', 'WebUI_Output', 'Extensions', 'Embeddings', 'VAE', 'TE',
        'CKPT', 'LORA', 'TMP_CKPT', 'TMP_LORA', 'Controlnet_Widget', 'Upscalers'
    ]
    for v in l:
        if v in globals(): del globals()[v]


def _var():
    F = {
        'Forge-Classic': (
            'extensions', 'embeddings', 'VAE', 
            'Stable-diffusion', 'Lora', 'ESRGAN', 
            None
        ),

        'Forge-Neo': (
            'extensions', 'embeddings', 'VAE', 
            'Stable-diffusion', 'Lora', 'ESRGAN', 
            'text_encoder'
        ),
    }

    ext, embed, vae, ckpt, lora, ups, te = F[ui]

    WebUI = HOME / ui
    Models = WebUI / 'models'

    WebUI_Output = WebUI / 'output'
    Extensions = WebUI / ext
    Embeddings = Models / embed

    VAE = Models / vae
    CKPT = Models / ckpt
    LORA = Models / lora
    Upscalers = Models / ups
    TE = Models / te if te else None

    return WebUI, Models, WebUI_Output, Extensions, Embeddings, VAE, CKPT, LORA, Upscalers, TE

if SSL:
    @register_line_magic
    def clear_output_images(line):
        _, _, output, _, _, _, _, _, _, _ = _var()
        SyS(f'rm -rf {output}/* ~/.cache/*')
        print(f'{ui} outputs cleared.')
        CD(HOME)

    @register_line_magic
    def uninstall_webui(line):
        SyS(f'rm -rf ~/{ui} ~/tmp ~/.cache/*')
        print(f'{ui} uninstalled.')
        CD(HOME)

        from util import restart_kernel
        restart_kernel()

if ui:
    _del()

    WebUI, Models, WebUI_Output, Extensions, Embeddings, VAE, CKPT, LORA, Upscalers, TE = _var()

    Controlnet_Widget = WebUI / 'asd/controlnet.py' if WebUI else None

    TMP_CKPT = TMP / 'ckpt'
    TMP_LORA = TMP / 'lora'

    tempe()
