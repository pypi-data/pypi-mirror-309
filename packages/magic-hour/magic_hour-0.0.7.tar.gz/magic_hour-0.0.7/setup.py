# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_hour',
 'magic_hour.core',
 'magic_hour.resources.v1',
 'magic_hour.resources.v1.ai_headshot_generator',
 'magic_hour.resources.v1.ai_image_generator',
 'magic_hour.resources.v1.ai_image_upscaler',
 'magic_hour.resources.v1.ai_qr_code_generator',
 'magic_hour.resources.v1.face_swap',
 'magic_hour.resources.v1.face_swap_photo',
 'magic_hour.resources.v1.files',
 'magic_hour.resources.v1.files.upload_urls',
 'magic_hour.resources.v1.image_projects',
 'magic_hour.resources.v1.image_to_video',
 'magic_hour.resources.v1.lip_sync',
 'magic_hour.resources.v1.text_to_video',
 'magic_hour.resources.v1.video_projects',
 'magic_hour.resources.v1.video_to_video',
 'magic_hour.types.models',
 'magic_hour.types.params']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.26.0,<0.27.0', 'pydantic>=2.5.0,<3.0.0', 'typing_extensions>=4.0.0']

setup_kwargs = {
    'name': 'magic-hour',
    'version': '0.0.7',
    'description': '',
    'long_description': '\n# Magic Hour API Python SDK\n\n\n## Overview\n\n# Introduction \n\nMagic Hour provides an API (beta) that can be integrated into your own application to generate videos using AI. \n\nWebhook documentation can be found [here](https://magichour.ai/docs/webhook).\n\nIf you have any questions, please reach out to us via [discord](https://discord.gg/JX5rgsZaJp).\n\n# Authentication\n\nEvery request requires an API key.\n\nTo get started, first generate your API key [here](https://magichour.ai/settings/developer).\n\nThen, add the `Authorization` header to the request.\n\n| Key | Value |\n|-|-|\n| Authorization | Bearer mhk_live_apikey |\n\n> **Warning**: any API call that renders a video will utilize frames in your account.\n\n\n\n### Synchronous Client\n\n```python\nfrom magic_hour import Client\nfrom os import getenv\n\nclient = Client(token=getenv("API_TOKEN"))\n```\n\n\n### Asynchronous Client\n\n```python\nfrom magic_hour import AsyncClient\nfrom os import getenv\n\nclient = AsyncClient(token=getenv("API_TOKEN"))\n```\n\n### SDK Usage \n See [SDK Examples](SDK_EXAMPLES.md) for example usage of all SDK functionality',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
