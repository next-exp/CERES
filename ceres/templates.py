import os
import logging

from ceres import versions

templates = {
    'irene' : {
        'csexample' : 'irene_CsProd_example.conf',
        'kr1300'    : 'irene_kr_s2_1300.conf'    ,
        'kr1300i'   : 'irene_kr_s2_1300i.conf'   ,
        'kr1500i'   : 'irene_kr_s2_1500i.conf'   ,
        'kr1650i'   : 'irene_kr_s2_1650i.conf'   ,
        'kr1900i'   : 'irene_kr_s2_1900i.conf'   ,
        'kr2200i'   : 'irene_kr_s2_2200i.conf'   ,
        'na_s1'     : 'irene_na_s1.conf'         ,
        'cs2000'    : 'irene_cs_s2_2000.conf'    ,
        'krth1300'  : 'irene_krth_s2_1300.conf'  ,
        'krth1600'  : 'irene_krth_s2_1600.conf'  ,
        'krth3200'  : 'irene_krth_s2_3200.conf'  ,
        'th2000'    : 'irene_th_s2_2000.conf'    ,
        'th1300'    : 'irene_th_s2_1300.conf'    ,
        'bg2000'    : 'irene_bg_s2_2000.conf'    ,
        'krbg1300'  : 'irene_krbg_s2_1300.conf'    ,
        'krbg1600'  : 'irene_krbg_s2_1600.conf'    ,
        'alpha_s1'  : 'irene_alpha_s1.conf'      ,
        'alpha_s2'  : 'irene_alpha_s2.conf'      ,
        'test'      : 'irene_test.conf',
        'krhighrate'      : 'irene_high_kr_rate.conf',
        'autotrigger'  : 'irene_autotrigger_1600.conf'
    },
    'dorothea' : {
        'csexample' : 'dorothea_example.conf',
        'kr'        : 'dorothea_kr.conf',
        'krth'      : 'dorothea_krth.conf',
        'krbg'      : 'dorothea_krbg.conf',
        'na_s1'     : 'dorothea_na.conf',
        'cs2000'    : 'dorothea_cs.conf',
        'th2000'    : 'dorothea_th.conf',
        'alpha'     : 'dorothea_alpha.conf',
        'krhighrate'     : 'dorothea_high_kr_rate.conf',
        'autotrigger'    : 'dorothea_autotrigger.conf',
    },
    'penthesilea' : {
        'bg'    : 'penthesilea_bg.conf',
        'th'        : 'penthesilea_228Th.conf'
    },
    'esmeralda' : {
        'bg'    : 'esmeralda_bg.conf'
    }
    
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

