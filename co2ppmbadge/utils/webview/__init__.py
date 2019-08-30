import os
import boto3

from datetime import timedelta

from jinja2 import Environment, PackageLoader, select_autoescape

JINJA_ENV = Environment(
    loader=PackageLoader('co2ppmbadge.utils.webview', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

BASE_URL = 'https://co2ppmbadge.piazza.energy'


def obj_finder(bucket_name, last_date, days_back=10, obj_name='ppm00.svg'):
    """obj_finder [summary]

    :param bucket_name: [description]
    :type bucket: [type]
    :param last_date: [description]
    :type last_date: [type]
    :param days_back: [description], defaults to 10
    :type days_back: int, optional
    :param obj_name: [description], defaults to 'ppm00.svg'
    :type obj_name: str, optional
    :return: [description]
    :rtype: [type]
    """
    obj_list = []
    bucket = boto3.resource('s3').Bucket(bucket_name)

    for i in range(days_back):
        date_src = last_date - timedelta(days=(i + 1))
        d_iso = date_src.isoformat()
        objs = bucket.objects.filter(Prefix=d_iso)
        for obj in objs:
            if obj.key.endswith(obj_name):
                obj_list.append({
                    obj_name: {
                        'date': d_iso,
                        'url': f'{BASE_URL}/{obj.key}',
                    }
                })
    return {
        'year': last_date.year,
        'date': last_date.isoformat(),
        'days': obj_list
    }


def html_creator(tmpl_data, path, f_name='index.html'):
    """html_creator [summary]

    :param tmpl_data: [description]
    :type tmpl_data: [type]
    :param path: [description]
    :type path: [type]
    :return: [description]
    :rtype: [type]
    """
    template = JINJA_ENV.get_template('base.html')
    output = template.render(**tmpl_data)
    with open(os.path.join(path, f_name), 'w') as f:
        f.write(output)
    return (path, f_name)
