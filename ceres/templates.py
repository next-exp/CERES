import os
import logging

from ceres import versions

templates = {
    'irene' : {
        'kr1300'   : 'irene_kr_1300.conf'   ,
        'nas1'     : 'irene_na_s1.conf'     ,
        'th2000'   : 'irene_th_s2_2000.conf',
    },
    'dorothea' : {
        'kr'     : 'dorothea_kr.conf'  ,
        'th2000' : 'dorothea_ths2.conf',
    }
}

def get_dir(version):
    base_path = ''
    if version == 'prod':
        base_path = os.environ['CERESDIR']
    else:
        base_path = os.environ['CERESDEVDIR']
    return os.path.join(base_path, 'templates/')

def get(city, template):
    version = versions.get_version()
    if not template in templates[city]:
        logging.error("Template {} not found for city {}".\
                      format(city, template))
        exit(1)
    template_file = get_dir(version) + templates[city][template]
    template = open(template_file).read()
    return template

def exec_template():
    version = versions.get_version()
    template_file = os.path.join(get_dir(version), 'exec.sh')
    template = open(template_file).read()
    return template

