from __future__ import division
from __future__ import print_function

import logging
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
    parser.add_argument('-ic','--ic-tag',
                        action   = 'store',
                        help     = 'ic tag for input files')
    parser.add_argument('-ceres','--ceres-tag',
                        action   = 'store',
                        help     = 'ceres tag for input files')
    parser.add_argument('-d','--debug',
                        action   = 'store_true',
                        help     = 'print debug information')
    parser.add_argument('-f','--file',
                        action   = 'store',
                        help     = 'file to process')
    return parser


#get options
args = get_parser().parse_args()
#set logging level
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logging.debug("Input arguments: {}".format(args))

#get tags
version        = versions.get_version()
templates_dir  = templates.get_dir(version)
ic_tag         = versions.get_ic_tag(templates_dir)
ceres_tag      = versions.get_ceres_tag()
versions       = data.Versions(ic      = ic_tag,
                               ceres   = ceres_tag,
                               config  = args.type,
                               version = version)
logging.debug(versions)
logging.info("You are running {} version with IC tag {} and CERES tag {}".
             format(version, ic_tag, ceres_tag))

#IO dirs
path_in  = utils.get_input_path(args, version)
base_dir = '/analysis/{}/hdf5/{}/{}/{}/'.format(args.run,
                                                version,
                                                ic_tag,
                                                ceres_tag)
path_out = base_dir + cities.outputs[args.city] + '/'
configs  = base_dir + 'configs/'
jobs_dir = base_dir + 'jobs/'
logs_dir = base_dir + 'logs/'

paths = data.Paths(input   = path_in,
                   output  = path_out,
                   configs = configs,
                   jobs    = jobs_dir,
                   logs    = logs_dir)
logging.debug(paths)
logging.info("Files from {} will be processed".format(paths.input))
logging.info("{} output files will be in {}".format(cities.outputs[args.city],
                                                     paths.output))

#check and make dirs
list(map(utils.check_make_dir, paths))

#remove old jobs
old_jobs = os.path.join(paths.jobs, args.city + '*sh')
list(map(os.remove, glob(old_jobs)))

#input files
if  args.file: files = utils.get_input_file(paths,args.file)
else         : files = utils.list_input_files(paths)

#generate configs files
config_files = jobs.generate_configs(files, args, paths, versions)

#generate job files
job_files = jobs.generate_jobs(config_files, args, paths, versions)

#submit jobs
if not args.do_not_submit:
    jobs.run_summary(job_files, args, paths, versions)
    jobs.submit(job_files, args)

logging.info("Done")
