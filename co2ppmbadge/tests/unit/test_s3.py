import os
import boto3
import tempfile
import mimetypes

from moto import mock_s3

from co2ppmbadge.utils.s3 import upload_file


@mock_s3
def test_empty_filename(monkeypatch):
    bucket_name = "MOCK_BUCKET"
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name)

    with tempfile.TemporaryDirectory() as tmpdirname:
        f_name = 'test.txt'
        f_path = os.path.join(tmpdirname, f_name)
        with open(f_path, 'w') as f:
            f.write('hello hello')
        upload_file(f_path, bucket_name)

    obj = s3.Object(bucket_name, f_path)
    obj.load()
    assert obj.content_length > 0
    assert obj.content_type == mimetypes.guess_type(f_name, strict=False)[0]


@mock_s3
def test_failed_upload():
    bucket_name = "I_DONT_EXIST"
    with tempfile.TemporaryDirectory() as tmpdirname:
        f_name = 'test.txt'
        f_path = os.path.join(tmpdirname, f_name)
        with open(f_path, 'w') as f:
            f.write('hello hello')
        out = upload_file(f_path, bucket_name)
        assert not out
