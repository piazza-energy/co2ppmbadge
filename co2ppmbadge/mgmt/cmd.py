""" provides some handy commands to run management tasks

AWS_DEFAULT_REGION
AWS_PROFILE

"""
import os
import boto3
import logging
from time import time
from dotenv import load_dotenv

from co2ppmbadge.utils.datasrc.hqcasanova import get_data

from . import create_upload_banners, create_upload_badges, create_upload_html

logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_dotenv()

S3_BUCKET = os.getenv('S3_BUCKET')
CDN_DISTRIBUTION_ID = os.getenv('CDN_DISTRIBUTION_ID')


def create_upload_assets():
    hqcasanova_data = get_data()
    date = hqcasanova_data['date'].date()
    banners = create_upload_banners(hqcasanova_data, S3_BUCKET)
    badges = create_upload_badges(hqcasanova_data, S3_BUCKET)
    create_upload_html(S3_BUCKET, date)
    logger.info(f'uploaded {banners}, {badges} and index.html')
    return {
        'data': {
            'bucket': S3_BUCKET,
            'keys': banners + badges + ['index.html'],
            'api': hqcasanova_data,
        }
    }


def invalidate_cache():
    client = boto3.client('cloudfront')
    response = client.create_invalidation(
        DistributionId=CDN_DISTRIBUTION_ID,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [
                    '/*',
                ]
            },
            'CallerReference': f'{time()}'
        }
    )
    logger.info(f'cdn invalidation {response}')
    return response
