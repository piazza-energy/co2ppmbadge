import boto3
import mimetypes

from co2ppmbadge.utils.datasrc import hqcasanova

from .fixtures import hqcasanova_static_data

from moto import mock_s3


@mock_s3
def test_create_upload_assets(hqcasanova_static_data, monkeypatch):
    bucket_name = "MOCK_BUCKET"

    # using static data as mock_s3 intercepts all calls to requests
    def mock_hqcasanova_data():
        return hqcasanova_static_data

    monkeypatch.setenv("S3_BUCKET", bucket_name)
    monkeypatch.setattr(hqcasanova, 'get_data', mock_hqcasanova_data)

    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name)

    from co2ppmbadge.mgmt.cmd import create_upload_assets
    resp = create_upload_assets()

    assert 'data' in resp
    assert 'bucket' in resp['data']
    assert 'keys' in resp['data']
    assert 'api' in resp['data']

    for k in resp['data']['keys']:
        obj = s3.Object(resp['data']['bucket'], k)
        obj.load()
        assert obj.content_length > 0
        assert obj.content_type == mimetypes.guess_type(k, strict=False)[0]
