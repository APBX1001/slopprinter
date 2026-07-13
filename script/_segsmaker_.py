from pathlib import Path

HOME = Path.home()
SRC = ''
TMP = Path('/tmp')

H = 'https://huggingface.co/gutris1/webui/resolve/main/env'

PY = {
    'FC': {
        'v': '3.11.15',
        'p': TMP / 'CLASSIC',
        'url': [
            f'{H}/FC-Torch2121-cu130-1.tar.lz4',
            f'{H}/FC-Torch2121-cu130-2.tar.lz4'
        ],
    },

    'FN': {
        'v': '3.13.12',
        'p': TMP / 'NEO',
        'url': [
            f'{H}/FN-Torch2121-cu130-1.tar.lz4',
            f'{H}/FN-Torch2121-cu130-2.tar.lz4'
        ],
    },
}

UID = {
    'Forge-Classic': {
        'repo': '-b classic https://github.com/Haoming02/sd-webui-forge-classic Forge-Classic',
        'branch': 'classic',

        'sym': lambda M: ['rm -rf ' + ' '.join(str(M / t) for _, t in LINKS['Forge-Classic'])],
        'links': lambda M: ((TMP / p, M / t) for p, t in LINKS['Forge-Classic']),

        'py': PY['FC'],

        'title': 'Forge Classic',
        'args': '--xformers --cuda-stream --persistent-patches',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'Forge-Neo': {
        'repo': '-b neo https://github.com/Haoming02/sd-webui-forge-classic Forge-Neo',
        'branch': 'neo',

        'py': PY['FN'],

        'title': 'Forge Neo',
        'args': '--xformers --cuda-stream',
        'cpu': '--cpu --skip-torch-cuda-test',
        'cm': True,
    },
}

LINKS = {
    'Forge-Classic': (
        ('ckpt', 'Stable-diffusion/tmp_ckpt'),
        ('lora', 'Lora/tmp_lora'),
        ('controlnet', 'ControlNet'),
    ),
}
