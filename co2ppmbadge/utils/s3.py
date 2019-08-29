import logging
import boto3
import mimetypes

from botocore.exceptions import ClientError

def upload_file(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket_name: Bucket name to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3 = boto3.resource('s3')
    try:
        mime = mimetypes.guess_type(file_name, strict=False)
        s3.Bucket(bucket_name).upload_file(
            file_name,
            object_name,
            ExtraArgs={'ContentType': mime[0]})
    except ClientError as e:
        logging.error(e)
        return False
    return True
