import os

from ceres import versions

templates = {
    'irene' : {
        'kr1300' : 'irene_kr_s2_1300.conf'
    },
    'dorothea' : {
        'kr1300' : 'dorothea_kr.conf'
    }
}

def get_dir(version):
    base_path = ''
    if version == 'prod':
        base_path = os.environ['CERESDIR']
    else:
        base_path = os.environ['CERESDEVDIR']
    return base_path + '/templates/'


def get(city, template):
    version = versions.get_version()
    template_file = get_dir(version) + templates[city][template]
    template = open(template_file).read()
    return template
