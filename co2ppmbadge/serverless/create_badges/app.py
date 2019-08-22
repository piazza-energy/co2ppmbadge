import os
import json
import tempfile
from dotenv import load_dotenv

from co2ppmbadge.utils.badges import create_badges_files
from co2ppmbadge.utils.datasrc.hqcasanova import get_data
from co2ppmbadge.utils.s3 import upload_file

load_dotenv()

S3_BUCKET = os.getenv('S3_BUCKET')


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    out = []
    hqcasanova_data = get_data()
    with tempfile.TemporaryDirectory() as tmpdirname:
        badges = create_badges_files(hqcasanova_data, tmpdirname)
        for f_name in badges['files']:
            d_iso = badges['date'].isoformat()
            local_file = os.path.join(badges['path'], f_name)
            upload_file(local_file, S3_BUCKET, f'latest/{f_name}')
            upload_file(local_file, S3_BUCKET, f'{d_iso}/{f_name}')
            out.append(f'latest/{f_name}')
            out.append(f'{d_iso}/{f_name}')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'data': {
                'bucket': S3_BUCKET,
                'keys': out,
            },
        }),
    }
