import boto3
import os
from datetime import date, timedelta
import tempfile

from moto import mock_s3

from co2ppmbadge.utils.webview import obj_finder, html_creator
from co2ppmbadge.utils.badges import get_svg_str

@mock_s3
def test_creator():
    bucket_name = "MOCK_BUCKET"
    f_name = 'ppm00.svg'
    today = date.today()
    day = today - timedelta(days=1)
    day_iso = day.isoformat()

    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name)
    object = s3.Object(bucket_name, f'{day_iso}/{f_name}')
    object.put(Body=get_svg_str(f'ppm {day_iso}', '410', 'red'))

    tmpl_data = obj_finder(bucket_name, today)
    assert 'days' in tmpl_data
    assert len(tmpl_data['days']) == 1
    assert f_name in tmpl_data['days'][0]
    assert 'url' in tmpl_data['days'][0][f_name]
    assert tmpl_data['days'][0][f_name]['url'].endswith(f'{day_iso}/{f_name}')

    with tempfile.TemporaryDirectory() as tmpdirname:
        path, html_file = html_creator(tmpl_data, tmpdirname)
        assert os.path.isfile(os.path.join(path, html_file))
        with open(os.path.join(path, html_file), 'r') as f:
            assert f'{day_iso}/{f_name}' in f.read()
