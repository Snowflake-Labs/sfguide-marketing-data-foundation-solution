import os
import base64


ASSETS = 'assets'


def image_b64(image_name: str):
    mime_type = image_name.split('.')[-1:][0].lower()
    if mime_type == 'svg':
        mime_type = mime_type+'+xml'
    image_path = get_asset_path(image_name)
    with open(image_path, 'rb') as f:
        bytes = f.read()
        content_b64enconded = base64.b64encode(bytes).decode()
        return f'data:image/{mime_type};base64,{content_b64enconded}'


def get_asset_path(asset_name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, os.pardir, ASSETS, asset_name))
