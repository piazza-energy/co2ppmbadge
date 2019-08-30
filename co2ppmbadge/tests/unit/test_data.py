import os
import tempfile

from co2ppmbadge.utils.badges import get_badges_dict, create_badges_files

from .fixtures import hqcasanova_data


def test_version():
    from co2ppmbadge.version import __version__
    assert __version__ == '1.0.0'


def test_hqcasanova(hqcasanova_data):
    assert hqcasanova_data['0'] > 400
    assert hqcasanova_data['1'] > 400
    # this test will fail at some point in the future :(
    assert hqcasanova_data['10'] < 400
    assert hqcasanova_data['units'] == 'ppm'
    for k in ['0', '1', '10', 'units', 'date', 'delta', 'all']:
        assert k in hqcasanova_data.keys()


def test_badges(hqcasanova_data):
    badges = get_badges_dict(hqcasanova_data, 'json')
    for k in ['ppm00', 'ppm01', 'ppm10']:
        assert k in badges.keys()


def test_badges_files(hqcasanova_data):
    with tempfile.TemporaryDirectory() as tmpdirname:
        badges = create_badges_files(hqcasanova_data, tmpdirname)
        for f in badges['files']:
            assert os.path.isfile(os.path.join(badges['path'], f))


def test_datahub():
    # check this out https://datahub.io/core/co2-ppm#python
    # from datapackage import Package
    # package = Package('https://datahub.io/core/co2-ppm/datapackage.json')

    # print list of all resources:
    # print(package.resource_names)
    # returns [
    #   'validation_report', 'co2-mm-mlo_csv', 'co2-annmean-mlo_csv', 'co2-gr-mlo_csv',
    #   'co2-mm-gl_csv', 'co2-annmean-gl_csv', 'co2-gr-gl_csv', 'co2-mm-mlo_json', 'co2-annmean-mlo_json',
    #   'co2-gr-mlo_json', 'co2-mm-gl_json', 'co2-annmean-gl_json', 'co2-gr-gl_json', 'co2-ppm_zip',
    #   'co2-mm-mlo', 'co2-annmean-mlo', 'co2-gr-mlo', 'co2-mm-gl', 'co2-annmean-gl', 'co2-gr-gl'
    # ]

    # print processed tabular data (if exists any)
    # for resource in package.resources:
    #     if resource.descriptor['datahub']['type'] == 'derived/json':
    #         print(resource.read())
    assert True
