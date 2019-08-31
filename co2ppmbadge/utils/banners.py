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
    draw.text((10, 120), f'{round(hqcasanova_data["1"], 2):.2f}', fill='white', font=font)
    draw.text((85, 120), f'{round(hqcasanova_data["10"], 2):.2f}', fill='white', font=font)

    # big text
    font = ImageFont.truetype(FONT, 36)
    draw.text((20, 45), f'{round(hqcasanova_data["0"], 2):.2f}', fill='white', font=font)
    return im


def banner_horiz(hqcasanova_data):
    dt = pendulum.instance(hqcasanova_data['date'])
    im = Image.new('RGB', (375, 65))
    draw = ImageDraw.Draw(im)
    # boxes
    draw.rectangle([(0,  0), (64, 64)], 'black', 'white', 1)
    draw.rectangle([(64, 0), (214,64)], 'coral', 'white', 1)
    draw.rectangle([(214,0), (294,64)], '#5B5B5B', 'white', 1)
    draw.rectangle([(294,0), (374,64)], '#5B5B5B', 'white', 1)

    # small text
    font = ImageFont.truetype(FONT, 12)
    draw.text((102, 8), dt.to_formatted_date_string(), fill='white', font=font)
    draw.text((240, 8), f'{int(dt.year) - 1}', fill='white', font=font)
    draw.text((320, 8), f'{int(dt.year) - 10}', fill='white', font=font)

    # medium text
    font = ImageFont.truetype(FONT, 20)
    draw.text((12, 6), 'CO2', fill='white', font=font)
    draw.text((12, 30), 'PPM', fill='white', font=font)
    draw.text((225, 30), f'{round(hqcasanova_data["1"], 2):.2f}', fill='white', font=font)
    draw.text((305, 30), f'{round(hqcasanova_data["10"], 2):.2f}', fill='white', font=font)

    # big text
    font = ImageFont.truetype(FONT, 36)
    draw.text((83, 15), f'{round(hqcasanova_data["0"], 2):.2f}', fill='white', font=font)
    return im


def banner_share(hqcasanova_data):
    dt = pendulum.instance(hqcasanova_data['date'])
    im = Image.new('RGB', (1000, 500))
    draw = ImageDraw.Draw(im)
    # boxes
    draw.rectangle([(0,    0), (600, 200)], 'black', 'white', 1)
    draw.rectangle([(600,  0), (999, 499)], 'coral', 'white', 1)
    draw.rectangle([(0,  200), (300, 499)], '#5B5B5B', 'white', 1)
    draw.rectangle([(300,200), (600, 499)], '#5B5B5B', 'white', 1)

    # small text
    font = ImageFont.truetype(FONT, 36)
    draw.text((110, 390), f'{int(dt.year) - 10}', fill='white', font=font)
    draw.text((410, 390), f'{int(dt.year) - 1}', fill='white', font=font)
    draw.text((700, 390), dt.to_formatted_date_string(), fill='white', font=font)

    # medium text
    font = ImageFont.truetype(FONT, 72)
    draw.text((35,   50), 'CO2', fill='white', font=font)
    draw.text((180,  50), 'PPM', fill='coral', font=font)
    draw.text((330,  50), 'BADGE', fill='white', font=font)
    draw.text((40,  280), f'{round(hqcasanova_data["1"], 2):.2f}', fill='white', font=font)
    draw.text((340, 280), f'{round(hqcasanova_data["10"], 2):.2f}', fill='white', font=font)

    # big text
    font = ImageFont.truetype(FONT, 108)
    draw.text((630, 165), f'{round(hqcasanova_data["0"], 2):.2f}', fill='white', font=font)
    return im


def create_banners_files(hqcasanova_data, path, prefix='banner', ext='png'):
    banner_types = ['sq', 'horiz', 'share']
    files = []
    for bt in banner_types:
        fn_name = f'{prefix}_{bt}'
        f_name = f'{prefix}_{bt}.{ext}'
        g_dict = globals()
        if fn_name in g_dict.keys():
            im = g_dict[fn_name](hqcasanova_data)
            im.save(os.path.join(path, f_name))
            files.append(f_name)
    return {
        'date': hqcasanova_data['date'].date(),
        'files': files,
        'path': path,
    }
