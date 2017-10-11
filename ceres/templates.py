import os
import logging

from ceres import versions

templates = {
    'diomira' : {
        'diomira' : 'diomira.conf'
    },
    'irene' : {
        'kr'   : 'irene_kr.conf',
        'na'   : 'irene_na.conf',
        'cs'   : 'irene_cs.conf',
        'tl'   : 'irene_tl.conf',
    },
    'dorothea' : {
        'kr'     : 'dorothea_kr.conf'  ,
        'na' : 'dorothea_na.conf',
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

def job_template():
    version = versions.get_version()
    template_file = os.path.join(get_dir(version), 'job.submit')
    template = open(template_file).read()
    return template

