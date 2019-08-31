import os
import tempfile

from co2ppmbadge.utils.badges import create_badges_files
from co2ppmbadge.utils.banners import create_banners_files
from co2ppmbadge.utils.s3 import upload_file
from co2ppmbadge.utils.webview import obj_finder, html_creator


def create_upload_banners(hqcasanova_data, s3_bucket):
    out = []
    # create banners
    with tempfile.TemporaryDirectory() as tmpdirname:
        banners = create_banners_files(hqcasanova_data, tmpdirname)
        for f_name in banners['files']:
            local_file = os.path.join(banners['path'], f_name)
            upload_file(local_file, s3_bucket, f'latest/{f_name}')
            out.append(f'latest/{f_name}')
    return out


def create_upload_badges(hqcasanova_data, s3_bucket):
    out = []
    # create badges
    with tempfile.TemporaryDirectory() as tmpdirname:
        badges = create_badges_files(hqcasanova_data, tmpdirname)
        for f_name in badges['files']:
            d_iso = badges['date'].isoformat()
            local_file = os.path.join(badges['path'], f_name)
            upload_file(local_file, s3_bucket, f'latest/{f_name}')
            upload_file(local_file, s3_bucket, f'{d_iso}/{f_name}')
            out.append(f'latest/{f_name}')
            out.append(f'{d_iso}/{f_name}')
    return out


def create_upload_html(s3_bucket, last_date):
    tmpl_data = obj_finder(s3_bucket, last_date)

    with tempfile.TemporaryDirectory() as tmpdirname:
        path, f_name = html_creator(tmpl_data, tmpdirname)
        upload_file(os.path.join(path, f_name), s3_bucket, f_name)
