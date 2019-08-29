import json
import pytest
import boto3
import mimetypes

from moto import mock_s3, mock_sns

from co2ppmbadge.utils.datasrc import hqcasanova

from .fixtures import apigw_event, sns_event, hqcasanova_static_data


@mock_s3
def test_create_webview_handler(sns_event, monkeypatch):
    bucket_name = "MOCK_BUCKET"
    monkeypatch.setenv("S3_BUCKET", bucket_name)
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name)

    from co2ppmbadge.serverless.create_webview import app
    app.lambda_handler(sns_event, None)

    key = 'index.html'
    obj = s3.Object(bucket_name, key)
    obj.load()
    assert obj.content_length > 0
    assert obj.content_type == mimetypes.guess_type(key, strict=False)[0]


@mock_sns
@mock_s3
def test_create_badges_handler(apigw_event, hqcasanova_static_data, monkeypatch):
    bucket_name = "MOCK_BUCKET"

    # using static data as mock_s3 intercepts all calls to requests
    def mock_hqcasanova_data():
        return hqcasanova_static_data

    # used to avoid NoRegionError when publishing to SNS
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'us-east-1')

    monkeypatch.setenv("S3_BUCKET", bucket_name)
    monkeypatch.setattr(hqcasanova, 'get_data', mock_hqcasanova_data)

    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name)

    sns = boto3.client('sns')
    sns_topic = sns.create_topic(Name="some-topic")
    monkeypatch.setenv("SNS_TOPIC_NEW_BADGES", sns_topic.get('TopicArn'))

    # importing it here so we can monkeypatch env vars
    from co2ppmbadge.serverless.create_badges import app

    resp = app.lambda_handler(apigw_event, None)
    resp_body = json.loads(resp['body'])

    assert resp['statusCode'] == 200
    assert 'data' in resp_body
    assert 'bucket' in resp_body['data']
    assert 'keys' in resp_body['data']

    for k in resp_body['data']['keys']:
        obj = s3.Object(resp_body['data']['bucket'], k)
        obj.load()
        assert obj.content_length > 0
        assert obj.content_type == mimetypes.guess_type(k, strict=False)[0]
