from __future__ import division
from __future__ import print_function

import os
import argparse
import magic
import re

from math       import ceil
from time       import sleep
from subprocess import check_output, call, CalledProcessError
from glob       import glob

def find_pattern(pattern, fname, group_name):
    result = ''
    data = open(fname).readlines()
    for line in data:
        pattern = re.compile(pattern)
        match = pattern.match(line)
        if match:
            result =  match.group(group_name)
            break
    return result

def get_parser():
    parser = argparse.ArgumentParser(description='Script to produce HDF5 files')
    parser.add_argument('-j','--jobs',
                        action   = 'store',
                        help     = 'jobs',
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

def checkmakedir(path):
    if os.path.isdir(path):
        print('hey, directory already exists!:\n' + path)
    else:
        os.makedirs(path)
        print('creating directory...\n' + path)

def get_index_from_file_name(name):
    return int(name.split('.')[-3].split('_')[0])

#Get CERES tag
cmd = 'git describe --tags'
output = check_output(cmd, shell=True, executable='/bin/bash')
ceres_tag = output.strip().split('\n')[0]

#Get IC tag
exec_template_file = '/home/icuser/CERES_dev/templates/irene.sh'
pattern = '(\s*)export(\s*)ICTDIR(\s*)=(\s*)(?P<icrepo>.*)'
icpath = find_pattern(pattern, exec_template_file, 'icrepo')
cmd = 'cd {}; git describe --tags'.format(icpath)
output = check_output(cmd, shell=True, executable='/bin/bash')
ic_tag = output.strip().split('\n')[0]

#get options
args = get_parser().parse_args()

jobs     = int(args.jobs)
run      = args.run
runtype  = args.type
nmax     = args.maxfiles
skip_sub = args.do_not_submit

#IO dirs
PATHIN     = '/analysis/{}/hdf5/data/'   .format(run)
PATHOUT    = '/analysis/{}_dev/hdf5/pmaps/'  .format(run)
CONFIGSDIR = '/analysis/{}_dev/hdf5/configs/'.format(run)
JOBSDIR    = '/analysis/{}_dev/hdf5/jobs/'   .format(run)
DSTDIR     = '/analysis/{}_dev/hdf5/dst/'    .format(run)

#----------- check and make dirs
checkmakedir(PATHIN)
checkmakedir(PATHOUT)
checkmakedir(CONFIGSDIR)
checkmakedir(JOBSDIR)
checkmakedir(DSTDIR)

#remove old jobs
map(os.remove, glob(JOBSDIR + '/*sh'))

#input files
files = glob(PATHIN + '/*h5')
files = sorted(files, key=get_index_from_file_name)

#open template
#TODO read from params

templates = {
    'csexample' : '/home/icuser/CERES_dev/templates/irene_CsProd_example.conf',
    'kr1300'    : '/home/icuser/CERES_dev/templates/irene_kr_s2_1300.conf',
    'cs2000'    : '/home/icuser/CERES_dev/templates/irene_cs_s2_2000.conf',
    'th2000'    : '/home/icuser/CERES_dev/templates/irene_th_s2_2000.conf',
    'bg2000'    : '/home/icuser/CERES_dev/templates/irene_bg_s2_2000.conf',
    'test'      : '/home/icuser/CERES_dev/templates/irene_test.conf'
}

# Pick from dict of templates. Otherwise assume it is the path to a template.
template_file = templates.get(runtype, runtype)
template      = open(template_file).read()
params        = {'pathin'  : PATHIN,
                 'pathout' : PATHOUT,
                 'run'     : run}

# build file list with outputs and filter it
to_process = []

#check hdf5 file are completely written
ftype = magic.Magic()
for f in files:
    #if file complete type would be: "Hierarchical Data Format (version 5) data"
    if ftype.from_file(f) == 'data':
        continue

    filename     = f.split('/')[-1]
    new_name     = 'pmaps_' + ic_tag + '_' + ceres_tag
    filename_out = filename.replace("dst_waves", new_name)

    #if file already exists, skip
    fout = PATHOUT + '/' + filename_out
    if os.path.isfile(fout):
        print("skip ", fout)
        continue

    params['filein' ] = filename
    params['fileout'] = filename_out

    config_file = CONFIGSDIR + '/' + filename + '.conf'
    print(config_file)
    open (config_file, 'w').write(template.format(**params))

    to_process.append(config_file)
    if len(to_process) == nmax:
        break

#Generate exec files
exec_template      = open(exec_template_file).read()
exec_params        = {'jobsdir': JOBSDIR}

jobfile    = file
nfiles     = int(ceil(len(to_process) * 1.0 / jobs))
count_jobs = 0
for i, config in enumerate(to_process):
    if i % nfiles == 0:
        if i:
            jobfile.write('\n\necho date\ndate\n')
            jobfile.close()

        jobfilename = JOBSDIR + '/irene_{}.sh'.format(count_jobs)
        jobfile     = open(jobfilename, 'w')
        jobfile.write(exec_template.format(**exec_params))
        count_jobs += 1

    cmd = 'city irene {}\n'.format(config)
    jobfile.write(cmd)
#sys.exit()

if not jobfile.closed:
    jobfile.close()

#send jobs
if not skip_sub:
    for i in range(count_jobs):
        cmd = 'qsub {}/irene_{}.sh'.format(JOBSDIR, i)
        print(cmd)
        call(cmd, shell=True, executable='/bin/bash')
        sleep(0.3)

#create dorothea job
templates_dst = {
'csexample' : '/home/icuser/CERES_dev/templates/dorothea_example.conf',
'kr1300'    : '/home/icuser/CERES_dev/templates/dorothea_kr.conf',
'cs2000'    : '/home/icuser/CERES_dev/templates/dorothea_cs.conf',
'th2000'    : '/home/icuser/CERES_dev/templates/dorothea_th.conf',
'bg2000'    : '/home/icuser/CERES_dev/templates/penthesilea_bg.conf'
}

if runtype in templates_dst:
    template_file = templates_dst[runtype]
    template = open(template_file).read()
    params = {'run': run}
    config_file = CONFIGSDIR + '/dorothea.conf'
    print(config_file)
    open(config_file, 'w').write(template.format(**params))

    jobfilename = JOBSDIR + '/' + 'dorothea.sh'
    jobfile = open(jobfilename, 'w')
    jobfile.write(exec_template.format(**exec_params))
    cmd = 'city dorothea {}\n'.format(config_file)
    jobfile.write(cmd)
