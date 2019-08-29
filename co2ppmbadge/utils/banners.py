import os
import pendulum

from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(os.path.dirname(__file__), 'fonts', 'Open Sans regular.ttf')


def banner_sq(hqcasanova_data):
    dt = pendulum.instance(hqcasanova_data['date'])
    im = Image.new('RGB', (155, 155))
    draw = ImageDraw.Draw(im)
    # boxes
    draw.rectangle([(0,  0), (154, 30)], 'black', 'white', 1)
    draw.rectangle([(0, 30), (154, 95)], 'coral', 'white', 1)
    draw.rectangle([(0, 95), ( 78,154)], '#5B5B5B', 'white', 1)
    draw.rectangle([(78,95), (154,154)], '#5B5B5B', 'white', 1)

    # small text
    font = ImageFont.truetype(FONT, 12)
    draw.text((40, 35), dt.to_formatted_date_string(), fill='white', font=font)
    draw.text((25, 100), f'{int(dt.year) - 1}', fill='white', font=font)
    draw.text((100, 100), f'{int(dt.year) - 10}', fill='white', font=font)

    # medium text
    font = ImageFont.truetype(FONT, 20)
    draw.text((35, 2), 'CO2 PPM', fill='white', font=font)
    draw.text((10, 120), f'{round(hqcasanova_data["1"], 2)}', fill='white', font=font)
    draw.text((85, 120), f'{round(hqcasanova_data["10"], 2)}', fill='white', font=font)

    # big text
    font = ImageFont.truetype(FONT, 36)
    draw.text((20, 45), f'{round(hqcasanova_data["0"], 2)}', fill='white', font=font)
    return im


def create_banners_files(hqcasanova_data, path, prefix='banner'):
    files = []
    im = banner_sq(hqcasanova_data)
    f_name = f'{prefix}_sq.png'
    im.save(os.path.join(path, f_name))
    files.append(f_name)
    return {
        'date': hqcasanova_data['date'].date(),
        'files': files,
        'path': path,
    }
