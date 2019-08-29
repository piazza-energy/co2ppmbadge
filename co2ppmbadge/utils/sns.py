import boto3


def send_sns_msg(topic_arn, msg):
    sns = boto3.client('sns')
    return sns.publish(
        TopicArn=topic_arn,
        Message=msg
    )
