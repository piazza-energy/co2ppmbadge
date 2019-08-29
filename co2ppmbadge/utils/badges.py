import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pybadges import badge


def get_svg_str(label, message, color):
    return badge(left_text=label, right_text=message, right_color=color)


def get_json_str(label, message, color):
    return json.dumps({
        'schemaVersion': 1,
        'label': label,
        'message': message,
        'color': color
    })


def get_badges_dict(hqcasanova_data, file_type):
    date = hqcasanova_data['date'].date()
    keys = [
        {
            'name': 'ppm00',
            'color': 'red',
            'field': '0',
            'date': date.isoformat()
        }, {
            'name': 'ppm01',
            'color': 'orange',
            'field': '1',
            'date': (date - relativedelta(years=1)).isoformat()
        }, {
            'name': 'ppm10',
            'color': 'blue',
            'field': '10',
            'date': (date - relativedelta(years=10)).isoformat()
        },
    ]
    func_catalogue = {
        'svg': get_svg_str,
        'json': get_json_str,
    }
    func = func_catalogue.get(file_type)
    return {
        d['name']: func(
            f'ppm {d["date"]}',
            str(hqcasanova_data[d['field']]),
            d['color'])
        for d in keys
    }

def create_badges_files(hqcasanova_data, path):
    date = hqcasanova_data['date'].date()
    files = []
    for file_type in ['svg', 'json']:
        # creates a dictionary of badges for both svg and json formats
        badges_dict = get_badges_dict(hqcasanova_data, file_type)
        for k, v in badges_dict.items():
            f_name = f'{k}.{file_type}'
            with open(os.path.join(path, f_name), 'w') as f:
                f.write(v)
                files.append(f_name)
    return {
        'date': date,
        'files': files,
        'path': path,
    }
