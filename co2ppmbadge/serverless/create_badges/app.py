import os
import tempfile
from dotenv import load_dotenv

from co2ppmbadge.serverless.formats import response_create_badges
from co2ppmbadge.utils.badges import create_badges_files
from co2ppmbadge.utils.banners import create_banners_files
from co2ppmbadge.utils.datasrc.hqcasanova import get_data
from co2ppmbadge.utils.s3 import upload_file
from co2ppmbadge.utils.sns import send_sns_msg

load_dotenv()

S3_BUCKET = os.getenv('S3_BUCKET')
SNS_TOPIC_NEW_BADGES = os.getenv('SNS_TOPIC_NEW_BADGES')


def lambda_handler(event, context):
    """lambda_handler create_badges: hit the hqcasanova endpoint, create badges, upload to s3, send sns notification

    this lambda is normally invoked via a daily cloudwatch event but can potentially be hooked to an API Gateway
    API Gateway Lambda Proxy Input Format https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    :param event: not used
    :type event: dict
    :param context: Lambda Context runtime methods and attributes https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    :type context: context object
    :return: API Gateway Lambda Proxy Output Format https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    :rtype: dict
    """
    out = []
    hqcasanova_data = get_data()
    with tempfile.TemporaryDirectory() as tmpdirname:
        # create banners
        banners = create_banners_files(hqcasanova_data, tmpdirname)
        for f_name in banners['files']:
            local_file = os.path.join(banners['path'], f_name)
            upload_file(local_file, S3_BUCKET, f'latest/{f_name}')
            out.append(f'latest/{f_name}')

        # create badges
        badges = create_badges_files(hqcasanova_data, tmpdirname)
        for f_name in badges['files']:
            d_iso = badges['date'].isoformat()
            local_file = os.path.join(badges['path'], f_name)
            upload_file(local_file, S3_BUCKET, f'latest/{f_name}')
            upload_file(local_file, S3_BUCKET, f'{d_iso}/{f_name}')
            out.append(f'latest/{f_name}')
            out.append(f'{d_iso}/{f_name}')

    msg = response_create_badges(
        hqcasanova_data['date'],
        S3_BUCKET,
        out)
    send_sns_msg(SNS_TOPIC_NEW_BADGES, msg)
    return {
        'statusCode': 200,
        'body': msg,
    }
