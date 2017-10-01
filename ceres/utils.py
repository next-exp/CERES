import re
import os
from glob import glob

def find_pattern(pattern, data, group_name):
    result = ''
    pattern = re.compile(pattern)
    match = pattern.match(data)
    if match:
        result =  match.group(group_name)
    return result

def find_pattern_in_file(pattern, fname, group_name):
    result = ''
    data = open(fname).readlines()
    for line in data:
        pattern = re.compile(pattern)
        match = pattern.match(line)
        if match:
            result =  match.group(group_name)
            break
    return result

def check_make_dir(path):
    if os.path.isdir(path):
        print('hey, directory already exists!:\n' + path)
    else:
        os.makedirs(path)
        print('creating directory...\n' + path)

def get_index_from_file_name(name):
    pattern = '(.*)[\._](?P<fileno>\d+)_(\d+)(.*)\.h5'
    return find_pattern(pattern, name, 'fileno')

def list_input_files(paths):
    files = glob(paths.input + '/*h5')
    files = sorted(files, key=get_index_from_file_name)
    return files

