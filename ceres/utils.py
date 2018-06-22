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

def get_index_from_file_name(name):
    if "pmaps" in name:
        pattern = '(.*)[\._](?P<fileno>\d+)_(\d+)(.*)\.h5'
    else:
        pattern = '(.*)[\._](\d+)_(?P<fileno>\d+)(.*)\.h5'
    return find_pattern(pattern, name, 'fileno')

def get_index_from_file_name(name):
    if "pmaps" in name:
        return name.split("/")[-1].split("_")[1]
    else:
        return name.split("/")[-1].split("_")[2]

def list_input_files(paths):
    files = glob(paths.input + '/*h5')
    files = sorted(files, key=get_index_from_file_name)
    return files

def get_input_file(paths,ifile):
    return glob(paths.input + '/*{:04d}*h5'.format(int(ifile)))

def get_input_path(args, version):
    path = '/analysis/{}/hdf5/'.format(args.run)
    if not os.path.isdir(path):
        logging.error('Waveforms files has not been processed yet for run {}, there are no input files for IC...'.\
                      format(args.run))
        exit(-1)

    if not args.city in cities.inputs:
        logging.error('Unkown city, please check spelling: {}'.format(args.city))
        exit(-1)

    # Irene always takes the same files while the rest of the cities
    # could take different versions of the pmaps
    if args.city == 'irene':
        path = join(path, 'data')
    else:
        path = join(path, version)
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
              {}'''.format(package, option, versions_dirs))
        exit(1)

    return join(path, versions_dirs[0])

def check_dir(path, args):
    if not os.path.isdir(path):
        logging.error('There are no files for {} with the IC & Ceres tags specified: {}, {}'.\
                      format(args.city, args.ic_tag, args.ceres_tag))
        exit(-1)
