from __future__ import division
from __future__ import print_function

import os
import argparse
import magic
from glob import glob

from ceres import versions
from ceres import templates
from ceres import cities
from ceres import utils
from ceres import data
from ceres import jobs

def get_parser():
    parser = argparse.ArgumentParser(description='Script to produce HDF5 files')
    parser.add_argument('-j','--jobs',
                        action   = 'store',
                        help     = 'jobs',
                        required = 'True')
    parser.add_argument('-c','--city',
                        action   = 'store',
                        help     = 'city',
                        required = 'True')
    parser.add_argument('-r','--run',
                        action   = 'store',
                        help     = 'run number',
                        required = 'True')
    parser.add_argument('-t','--type',
                        action   = 'store',
                        help     = 'run type',
                        required = 'True')
    parser.add_argument('-m','--maxfiles',
                        action   = 'store',
                        help     = 'maximum number of files to be processed',
                        default  = float("inf"))
    parser.add_argument('-x','--do-not-submit',
                        action   = 'store_true',
                        help     = 'skip job submission if present')
    return parser


#get options
args = get_parser().parse_args()
print (args)

#get tags
version        = versions.get_version()
templates_dir  = templates.get_dir(version)
ic_tag         = versions.get_ic_tag(templates_dir)
ceres_tag      = versions.get_ceres_tag()
versions       = data.Versions(ic        = ic_tag,
                               ceres = ceres_tag,
                               config    = args.type)

#IO dirs
#TODO: choose input dir (ictag, version, city...)
path_in  = '/analysis/{}/hdf5/data/'   .format(args.run)
base_dir = '/analysis/{}/hdf5/{}/{}/{}/'.format(args.run, version, ic_tag, ceres_tag)
path_out = base_dir + cities.outputs[args.city] + '/'
configs  = base_dir + 'configs/'
jobs_dir = base_dir + 'jobs/'

paths = data.Paths(input = path_in,
                   output     = path_out,
                   configs = configs,
                   jobs    = jobs_dir)
print(paths)

#check and make dirs
map(utils.check_make_dir, paths)

#remove old jobs
map(os.remove, glob(paths.jobs + '/*sh'))

#input files
files = utils.list_input_files(paths)
print(files)

#choose template


#TODO: Choose 1to1 or allto1
jobs.generate_configs(files, args, paths, versions)
