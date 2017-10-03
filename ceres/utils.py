import re
import os
from os.path import join
from glob    import glob

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

def get_input_path(args, version):
    path = ''
    # Irene always takes the same files while the rest of the cities
    # could take different versions of the pmaps
    if args.city == 'irene':
        path = '/analysis/{}/hdf5/data/'.format(args.run)
    else:
        path = '/analysis/{}/hdf5/{}'.format(args.run, version)
        #Scan for IC versions
        if args.ic_tag:
            path = join(path, args.ic_tag)
        else:
            path = scan_dirs(path, 'IC')
        #Scan for CERES versions
        if args.ceres_tag:
            path = join(path, args.ceres_tag)
        else:
            path = scan_dirs(path, 'CERES')

    return path

def scan_dirs(path, package):
    print path
    dirs = os.listdir(path)
    versions_dirs = [d for d in dirs if os.path.isdir(join(path, d))]
    print versions_dirs

    if len(versions_dirs) > 1:
        option = '-' + package.lower()
        print('''Please choose an {} version for the input files using {} option:
              {}''').format(package, option, versions_dirs)
        exit(1)

    return join(path, versions_dirs[0])

