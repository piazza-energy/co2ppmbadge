import json


def response_create_badges(dt, bucket, keys, dumps=True):
    out = {
        'data': {
            'date': dt.isoformat(),
            'bucket': bucket,
            'keys': keys,
        }
    }
    return json.dumps(out) if dumps else out
