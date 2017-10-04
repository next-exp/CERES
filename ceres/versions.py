from subprocess import check_output, call, CalledProcessError
import os
import logging

from ceres import utils

#get CERES tag
def get_ceres_tag():
    cmd = 'git describe --tags'
    unstaged_changes()
    output = check_output(cmd, shell=True, executable='/bin/bash')
    ceres_tag = output.strip().split('\n')[0]
    return ceres_tag

#get CERES version (prod/dev)
def get_version():
    cmd     = "git branch | awk '/\*/ { print $2; }'"
    output  = check_output(cmd, shell=True, executable='/bin/bash')
    branch  = output.strip().split('\n')[0]
    version = 'dev' if 'dev' in branch else 'prod'
    return version

#get IC tag
def get_ic_tag(templates):
    exec_template_file = os.path.join(templates, 'exec.sh')
    pattern = '(\s*)export(\s*)ICTDIR(\s*)=(\s*)(?P<icrepo>.*)'
    icpath = utils.find_pattern_in_file(pattern, exec_template_file, 'icrepo')
    cmd = 'cd {}; git describe --tags'.format(icpath)
    output = check_output(cmd, shell=True, executable='/bin/bash')
    ic_tag = output.strip().split('\n')[0]
    return ic_tag

#check there are no unstaged changes
def unstaged_changes():
    cmd = 'git diff --name-only'
    output = check_output(cmd, shell=True, executable='/bin/bash')
    files  = output.strip().split('\n')
    if files[0] != '':
        message  = 'You have modified files that are not included in a commit.'
        message += 'Please do it with:\n'
        message += '\tgit add <files>\n'
        message += '\tgit commit -m "short description"\n'
        message += 'This are the files:\n\t'
        for f in files:
            message += f + ' '
        logging.warning(message)

