import os
import logging

from ceres import versions

templates = {
    'hypathia':   {'hypathia_def' : 'hypathia_def.conf'},
    'irene' :     {'irene_def'    : 'irene_def.conf',
                   'ArConf'       : 'irene_Ar.conf',
                   'ArLowEConf'   : 'irene_Ar_LowEnergy.conf'},
    'dorothea' :  {'dorothea_def' : 'dorothea_def.conf',
                   'ArConf'       : 'dorothea_Ar.conf',},
    'sophronia' : {'sophronia_def': 'sophronia_def.conf',
                   'ArConf'       : 'sophronia_Ar.conf',
                   'ArLowEConf'   : 'sophronia_Ar_LowEnergy.conf'},
    'esmeralda' : {'esmeralda_def': 'esmeralda_def.conf',
                   'ArConf'       : 'esmeralda_Ar.conf'}

}

city_memory = {
    'hypathia': '5gb',
    'irene' : '1gb',
    'dorothea' :'5gb',
    'sophronia' : '5gb',
    'esmeralda' : '5gb',
}

def get_dir(version):
    base_path = ''
    if version == 'prod':
        base_path = os.environ['CERESDIR']
    else:
        base_path = os.environ['CERESDEVDIR']
    return os.path.join(base_path, 'templates/')

def getTemplateFilename(city, template):
    version = versions.get_version()
    if not template in templates[city]:
        logging.error("Template {} not found for city {}".\
                      format(city, template))
        exit(1)
    template_file = templates[city][template]
    return template_file

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

def summary_template():
    version = versions.get_version()
    template_file = os.path.join(get_dir(version), 'run_summary.py')
    template_py = open(template_file).read()

    template_file = os.path.join(get_dir(version), 'run_summary.sh')
    template_sh = open(template_file).read()
    return template_py, template_sh

