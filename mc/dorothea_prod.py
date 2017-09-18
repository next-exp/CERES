from __future__ import print_function

import argparse
from time import sleep
from subprocess import call
import sys, os
from datetime import datetime
from os.path import dirname
from glob import glob


def get_parser(args=None):
    parser = argparse.ArgumentParser(description='Script to produce HDF5 files')
    parser.add_argument('-i','--inputpath',
                        action='store',
                        help='input path',
                        required='True')
    parser.add_argument('-o','--outputpath',
                        action='store',
                        help='output path',
                        required='True')
    parser.add_argument('-t','--type',
                        action='store',
                        help='run type',
                        required='True')
    parser.add_argument('-c','--configpath',
                        action='store',
                        help='config path',
                        required='True')
    return parser


#get options
args = get_parser().parse_args()
opts = vars(args) # dict
print(args)

input_path = args.inputpath
output_path = args.outputpath
output_path = args.outputpath
config_path = args.configpath
runtype = args.type

configs = config_path + '/config'
exes = config_path + '/exec'
jobs = config_path + '/jobs'
logs = config_path + '/logs'


#----------- check and make dirs
def checkmakedir( path ):
    if os.path.isdir( path ):
        print('hey, directory already exists!:\n' + path)
    else:
        os.makedirs( path )
        print('creating directory...\n' + path)

checkmakedir(configs)
checkmakedir(exes)
checkmakedir(jobs)
checkmakedir(logs)

#input files
files = glob(input_path + '/*h5')
files = [f.split('/')[-1] for f in files]
#files = sorted(files, key=lambda s: int(s.split('.')[-3].split('_')[0]))
print( files)

#open template
templates = { 'kr' : '/afs/cern.ch/user/j/jobenllo/newprod/templates/dorothea_kr.conf',
              'na' : '/afs/cern.ch/user/j/jobenllo/newprod/templates/dorothea_na.conf'}

#template_file = '/home/icuser/production/templates/irene_3645.conf'
if runtype in templates:
    template_file = templates[runtype]
else:
    template_file = runtype

template = open(template_file).read()
exec_template_file = '/afs/cern.ch/user/j/jobenllo/newprod/templates/exec.sh'
exec_template = open(exec_template_file).read()

job_template_file = '/afs/cern.ch/user/j/jobenllo/newprod/templates/job.submit'
job_template = open(job_template_file).read()

for f in files:
    config_filename = configs + '/' + f + '.conf'
    exec_filename   = exes + '/' + f + '.sh'
    job_filename    = jobs + '/' + f + '.submit'
    output_filename = logs + '/' + f + '.out'
    error_filename  = logs + '/' + f + '.err'
    log_filename    = logs + '/' + f + '.log'

    fileout = f.split('.')[0].split('_')
    fileout[-2] = 'kDST'
    fileout = '_'.join(fileout) + '.h5'
    print (fileout)

    params = {'filein'  : f,
              'fileout' : fileout}

    #write config
    open(config_filename, 'w').write(template.format(**params))

    params = {'filein'     : f,
              'fileout'    : fileout,
              'pathin'     : input_path,
              'pathout'    : output_path,
              'city'       : 'dorothea',
              'configfile' : config_filename}

    #write exec
    open(exec_filename, 'w').write(exec_template.format(**params))


    params = {'exec'   : exec_filename,
              'output' : output_filename,
              'err'    : error_filename,
              'log'    : log_filename}
    #write job file
    open(job_filename, 'w').write(job_template.format(**params))
