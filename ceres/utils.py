import re
import logging
import os
from os.path import join
from glob    import glob
from ceres   import cities

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
        logging.debug('directory already exists!: ' + path)
    else:
        os.makedirs(path)
        logging.debug('creating directory: ' + path)

#Hack to include both indexes & pressure
def get_index_from_file_name(name):
    pattern = '(.*)[\._](?P<fileno>\d+_\d+_\dbar)(.*)\.h5'
    return find_pattern(pattern, name, 'fileno')

def list_input_files(paths):
    files = glob(paths.input + '/*h5')
    files = sorted(files, key=get_index_from_file_name)
    return files

def get_input_path(args, version):
    path = '/eos/experiment/next/productions/{}/'.format(args.isotope)
    if not os.path.isdir(path):
        logging.error('{} input files for diomira not found...'.\
                      format(args.isotope))
        exit(-1)

    if not args.city in cities.inputs:
        logging.error('Unkown city, please check spelling: {}'.format(args.city))
        exit(-1)

    # Irene always takes the same files while the rest of the cities
    # could take different versions of the pmaps
    if args.city == 'diomira':
        path = join(path, args.next_tag , cities.inputs['diomira'])
    else:
        check_dir(path, args)
        #Scan for IC versions
        if args.ic_tag:
            path = join(path, args.ic_tag)
        else:
            path = scan_dirs(path, 'IC')
        check_dir(path, args)
        #Scan for CERES versions
        if args.ceres_tag:
            path = join(path, args.ceres_tag)
        else:
            path = scan_dirs(path, 'CERES')
        path = join(path, cities.inputs[args.city])
        check_dir(path, args)
    return path

def scan_dirs(path, package):
    dirs = os.listdir(path)
    versions_dirs = [d for d in dirs if os.path.isdir(join(path, d))]
    logging.debug("{} versions: {}".format(package, versions_dirs))

    if len(versions_dirs) > 1:
        option = '-' + package.lower()
        logging.error("Cannot decide which input files version to use...")
        print('''Please choose an {} version for the input files using {} option:
              {}''').format(package, option, versions_dirs)
        exit(1)

    return join(path, versions_dirs[0])

def check_dir(path, args):
    if not os.path.isdir(path):
        logging.error('There are no files for {} with the IC & Ceres tags specified: {}, {}'.\
                      format(args.city, args.ic_tag, args.ceres_tag))
        exit(-1)
