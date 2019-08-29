import os
import tempfile

from PIL import Image

from co2ppmbadge.utils.banners import create_banners_files

from .fixtures import hqcasanova_static_data


def test_banner_sq(hqcasanova_static_data):
    banners_output = [{
        'size': (155, 155),
        'mode': 'RGB',
    }]
    with tempfile.TemporaryDirectory() as tmpdirname:
        banners = create_banners_files(hqcasanova_static_data, tmpdirname)
        for i, f_name in enumerate(banners['files']):
            im = Image.open(os.path.join(tmpdirname, f_name))
            assert im.size == banners_output[i]['size']
            assert im.mode == banners_output[i]['mode']
