import json
import pytest

from datetime import datetime, date, timezone

from co2ppmbadge.utils.datasrc.hqcasanova import get_data


@pytest.fixture(scope='session')
def hqcasanova_data():
    """hqcasanova_data returns a dictionary from the live api to be used as fixture

    :return: [description]
    :rtype: [type]
    """
    return get_data()


@pytest.fixture(scope='session')
def hqcasanova_static_data():
    """hqcasanova_data returns a static dictionary to be used as fixture

    :return: [description]
    :rtype: [type]
    """
    return {
        '0': 410.24,
        '1': 407.07,
        '10': 385.95,
        'units': 'ppm',
        'date': datetime.now(timezone.utc),
        'delta': 5.47,
        'all': 'Up-to-date weekly average CO2 at Mauna Loa\nWeek starting on August 11, 2019: 410.24 ppm\nWeekly value from 1 year ago: 407.07 ppm\nWeekly value from 10 years ago: 385.95 ppm'
    }


@pytest.fixture
def sns_event():
    message = json.dumps({
        'data': {
            'date': date.today().isoformat(),
            'bucket': 'MOCK_BUCKET',
            'keys': [f'latest/{f_name}' for f_name in ['ppm00.svg', 'ppm01.svg', 'ppm10.svg']]
        }
    })
    return {
        "Records":[
            {
                "EventSource":"aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:us-east-1:123456789012:lambda_topic:0b6941c3-f04d-4d3e-a66d-b1df00e1e381",
                "Sns":{
                    "Type": "Notification",
                    "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                    "TopicArn": "arn:aws:sns:us-east-1:123456789012:lambda_topic",
                    "Subject": "TestInvoke",
                    "Message": message,
                    "Timestamp": "2019-04-02T07:36:57.451Z",
                    "SignatureVersion": "1",
                    "Signature": "r0Dc5YVHuAglGcmZ9Q7SpFb2PuRDFmJNprJlAEEk8CzSq9Btu8U7dxOu++uU",
                    "SigningCertUrl": "http://sns.us-east-1.amazonaws.com/SimpleNotificationService-d6d679a1d18e95c2f9ffcf11f4f9e198.pem",
                    "UnsubscribeUrl": "http://cloudcast.amazon.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:123456789012:example_topic:0b6941c3-f04d-4d3e-a66d-b1df00e1e381",
                    "MessageAttributes": {"key":{"Type":"String","Value":"value"}}
                }
            }
        ]
    }


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "test": "body" }',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }
