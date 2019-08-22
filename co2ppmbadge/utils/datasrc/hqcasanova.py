import re
import json
import requests
import pendulum

API_URL = 'http://hqcasanova.com/co2/?callback=cb'


def parse_data(data_dict):
    """parse_data reads a hqcasanova_dict and returns it with parsed data
    i.e. string to float and isoformat to datetime

    expecting the following input
    {
      "0":"413.98",
      "1":"411.22",
      "10":"390.17",
      "units":"ppm",
      "date":"2019-06-20T13:02:27+02:00",
      "delta":5.41,
      "all":"Up-to-date weekly average CO2 at Mauna Loa\\nWeek starting on June 9, 2019: 413.98 ppm\\nWeekly value from 1 year ago: 411.22 ppm\\nWeekly value from 10 years ago: 390.17 ppm"
    }

    :param data_dict: input dict as described
    :type data_dict: dict
    :return: output dict with parsed values
    :rtype: dict
    """
    for key in ['0', '1', '10']:
        data_dict[key] = float(data_dict[key])
    data_dict['date'] = pendulum.parse(data_dict['date'])
    return data_dict


def get_data():
    """get_data invokes the api and parses the result

    :return: a parsed data dict with float values for ppm and datetime for date
    :rtype: dict
    """
    r = requests.get(API_URL)
    m = re.match(r'cb\((?P<json>.*)\)', r.text)
    out = json.loads(m.group('json'))
    return parse_data(out)
