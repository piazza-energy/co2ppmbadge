import os
import json
import logging
import pendulum
from dotenv import load_dotenv

from co2ppmbadge.mgmt import create_upload_html

logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_dotenv()

S3_BUCKET = os.getenv('S3_BUCKET')


def lambda_handler(event, context):
    """lambda_handler create_webview: reads the date from the sns event, fetches badges on s3
    in a date range ending with the parameter received and formats the archive section of an index.html accordingly

    :param event: an SNS event, have a look at https://aws.amazon.com/blogs/mobile/invoking-aws-lambda-functions-via-amazon-sns/
    :type event: dict
    :param context: Lambda Context runtime methods and attributes https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    :type context: context object
    """
    event_data = json.loads(event['Records'][0]['Sns']['Message'])
    last_date = pendulum.parse(event_data['data']['date']).date()
    logger.info(f'creating index file for {last_date}')
    create_upload_html(S3_BUCKET, last_date)
