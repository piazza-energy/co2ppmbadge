import json
import pytest
import boto3
import mimetypes

from moto import mock_s3

from co2ppmbadge.utils.datasrc import hqcasanova

from .fixtures import apigw_event, hqcasanova_static_data


@mock_s3
def test_lambda_handler(apigw_event, hqcasanova_static_data, monkeypatch):
    bucket_name = "MOCK_BUCKET"

    # using static data as mock_s3 intercepts all calls to requests
    def mock_hqcasanova_data():
        return hqcasanova_static_data

    monkeypatch.setenv("S3_BUCKET", bucket_name)
    monkeypatch.setattr(hqcasanova, 'get_data', mock_hqcasanova_data)

    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name)

    # importing it here so we can monkeypatch env vars
    from co2ppmbadge.serverless.create_badges import app

    resp = app.lambda_handler(apigw_event, "")
    body = json.loads(resp['body'])

    assert resp['statusCode'] == 200
    assert 'data' in body
    assert 'bucket' in body['data']
    assert 'keys' in body['data']

    for k in body['data']['keys']:
        obj = s3.Object(body['data']['bucket'], k)
        obj.load()
        assert obj.content_length > 0
        assert obj.content_type == mimetypes.guess_type(k, strict=False)[0]
