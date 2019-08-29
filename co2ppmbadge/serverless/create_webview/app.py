import os
import json
import tempfile
import pendulum
from dotenv import load_dotenv

from co2ppmbadge.utils.webview import obj_finder, html_creator
from co2ppmbadge.utils.s3 import upload_file

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
    print(f'creating index file for {last_date}')
    tmpl_data = obj_finder(S3_BUCKET, last_date)
    with tempfile.TemporaryDirectory() as tmpdirname:
        path, f_name = html_creator(tmpl_data, tmpdirname)
        upload_file(os.path.join(path, f_name), S3_BUCKET, f_name)
