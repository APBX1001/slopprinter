from IPython.display import clear_output
from IPython import get_ipython
from pathlib import Path
import subprocess
import argparse
import logging
import shutil
import shlex
import json
import yaml
import time
import os

from _segsmaker_ import HOME, SRC, UID
from cupang import Tunnel as Alice

SyS = get_ipython().system
iRON = os.environ

ROOT = Path.home()
CWD = Path.cwd()
PW = '82a973c04367123ae98bd9abdf80d9eda9b910e2'

MARK = SRC / 'marking.json'
ui = json.load(MARK.open()).get('ui')

KAGGLE = 'KAGGLE_DATA_PROXY_TOKEN' in iRON

def trashing():
    f = ['ckpt', 'lora', 'controlnet', 'svd', 'z123']
    for p in [HOME / ui] + [Path('/tmp') / d for d in f]:
        SyS(f'find {p} -type d -name .ipynb_checkpoints -exec rm -rf {{}} + > /dev/null 2>&1')

def NGROK_auth(token):
    yml = ROOT / '.config/ngrok/ngrok.yml'

    if yml.exists(): current_token = yaml.safe_load(yml.read_text()).get('agent', {}).get('authtoken')
    else: current_token = None

    if current_token != token: SyS(f'ngrok config add-authtoken {token}'); print()

def ZROK_enable(token):
    zrok_env = ROOT / '.zrok2/environment.json'
    e = f'zrok2 enable {token}'
    d = 'zrok2 disable'

    if zrok_env.exists():
        current_token = json.loads(zrok_env.read_text()).get('zrok_token')
        if current_token != token: SyS(d); SyS(e); print()

    else: SyS(e); print()

def webui_launch(launch_args, ngrok_token=None, zrok_token=None):
    iRON['PYTHONWARNINGS'] = 'ignore'

    SyS(f"echo -n {int(time.time()) + 3600} > {CWD / 'asd/pinggytimer.txt'}")
    launch_args += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'

    if '--share' in launch_args: launch_args = launch_args.replace('--share', '')
    if KAGGLE: launch_args += f' --encrypt-pass={PW}'

    if ui == 'Forge-Neo':
        iRON['MPLBACKEND'] = 'agg'

    iRON.setdefault('IIB_ACCESS_CONTROL', 'disable')
    iRON.setdefault('IIB_SKIP_OPTIONAL_DEPS', '1')

    cmd = f'python3 launch.py {launch_args}'

    port = UID[ui].get('port', 7860)

    cloudflared = f'cl tunnel --url localhost:{port}'
    pinggy = f'ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io'
    ngrok = f'ngrok http http://localhost:{port} --log stdout'
    zrok2 = f'zrok2 share public localhost:{port} --headless'
    gradio = f'gradio-tun {port}'

    Zuberg = Alice(port)
    Zuberg.logger.setLevel(logging.DEBUG)
    Add = lambda command, name, pattern: Zuberg.add_tunnel(command=command, name=name, pattern=pattern)

    if not (ngrok_token or zrok_token):
        Add(gradio, 'Gradio', r'https://[\w-]+\.gradio\.live')
        Add(pinggy, 'Pinggy', r'https://[\w-]+\.run\.pinggy-free\.link')
        Add(cloudflared, 'Cloudflared', r'[\w-]+\.trycloudflare\.com')

    if ngrok_token:
        NGROK_auth(ngrok_token)
        Add(ngrok, 'NGROK', r'https://[\w-]+\.ngrok-free\.[\w.-]+')

    if zrok_token:
        ZROK_enable(zrok_token)
        Add(zrok2, 'ZROK2', r'[\w-]+\.shares\.zrok\.io')

    with Zuberg:
        SyS(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='nothing to read here')
    parser.add_argument('--N', type=str, help='NGROK tunnel (pass a token or do nothing)', default=None)
    parser.add_argument('--Z', type=str, help='ZROK2 tunnel (pass a token or do nothing)', default=None)

    args, unknown = parser.parse_known_args()
    launch_args = ' '.join(unknown)

    try:
        trashing()
        webui_launch(launch_args, args.N, args.Z)
    except KeyboardInterrupt:
        pass
