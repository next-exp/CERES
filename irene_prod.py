from __future__ import division
from __future__ import print_function

import os
import argparse
import magic

from math       import ceil
from time       import sleep
from subprocess import call
from glob       import glob


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


#get options
args = get_parser().parse_args()

jobs     = int(args.jobs)
run      = args.run
runtype  = args.type
nmax     = args.maxfiles
skip_sub = args.do_not_submit

#IO dirs
PATHIN     = '/analysis/{}/hdf5/data/'   .format(run)
PATHOUT    = '/analysis/{}/hdf5/pmaps/'  .format(run)
CONFIGSDIR = '/analysis/{}/hdf5/configs/'.format(run)
JOBSDIR    = '/analysis/{}/hdf5/jobs/'   .format(run)
DSTDIR     = '/analysis/{}/hdf5/dst/'    .format(run)

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

templates = { 'alpha'    : '/home/icuser/production/templates/irene_alpha.conf'     ,
              'alpha3200': '/home/icuser/production/templates/irene_alpha_3200.conf',
              'alpha_s1' : '/home/icuser/production/templates/irene_alpha_s1.conf'  ,
              'alpha800' : '/home/icuser/production/templates/irene_alpha_800.conf' ,
              'na'       : '/home/icuser/production/templates/irene_na.conf'        ,
              'kr3200'   : '/home/icuser/production/templates/irene_kr_3200.conf'   ,
              'kr1300'   : '/home/icuser/production/templates/irene_kr_1300.conf'   ,
              'co'       : '/home/icuser/production/templates/irene_co.conf'        ,
              'co2ms'    : '/home/icuser/production/templates/irene_co_2ms.conf'    ,
              'nas1'     : '/home/icuser/production/templates/irene_na_s1.conf'     ,
              'nas1_200' : '/home/icuser/production/templates/irene_na_s1_200.conf' ,
              'nas2'     : '/home/icuser/production/templates/irene_na_s2.conf'     ,
              'nas21600' : '/home/icuser/production/templates/irene_na_s2_1600.conf',
              'cs1300'   : '/home/icuser/production/templates/irene_cs_s2_1300.conf',
              'cs2000'   : '/home/icuser/production/templates/irene_cs_s2_2000.conf',
              'th2000'   : '/home/icuser/production/templates/irene_th_s2_2000.conf',
              'bg2000'   : '/home/icuser/production/templates/irene_bg_s2_2000.conf'}

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
    filename_out = filename.replace("dst_waves", "pmaps")

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

exec_template_file = '/home/icuser/production/templates/irene.sh'
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

    cmd = 'python $ICDIR/cities/irene.py -c {}\n'.format(config)
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
templates_dst = { 'alpha'    : '/home/icuser/production/templates/dorothea_alpha.conf'   ,
                  'alpha800' : '/home/icuser/production/templates/dorothea_alpha.conf'   ,
                  'alpha_s1' : '/home/icuser/production/templates/dorothea_alpha.conf'   ,
                  'nas1'     : '/home/icuser/production/templates/dorothea_nas1.conf'    ,
                  'nas1_200' : '/home/icuser/production/templates/dorothea_nas1_200.conf',
                  'co'       : '/home/icuser/production/templates/dorothea_co.conf'      ,
                  'kr3200'   : '/home/icuser/production/templates/dorothea_kr.conf'      ,
                  'kr1300'   : '/home/icuser/production/templates/dorothea_kr.conf'      ,
                  'nas2'     : '/home/icuser/production/templates/dorothea_nas2.conf'    ,
                  'nas21600' : '/home/icuser/production/templates/dorothea_nas2.conf'    ,
                  'cs1300'   : '/home/icuser/production/templates/dorothea_css2.conf'    ,
                  'cs2000'   : '/home/icuser/production/templates/dorothea_css2.conf'    ,
                  'th2000'   : '/home/icuser/production/templates/dorothea_ths2.conf'    ,
                  'bg2000'   : '/home/icuser/production/templates/dorothea_bgs2.conf'    }

if runtype in templates_dst:
    template_file = templates_dst[runtype]

    template    = open(template_file).read()
    params      = {'run': run,
                   'pathin': PATHIN.replace("data", "pmaps"),
                   'pathout': PATHOUT.replace("pmaps", "dst")}
    config_file = CONFIGSDIR + '/dorothea.conf'

    print(config_file)
    open (config_file, 'w').write(template.format(**params))

    jobfilename = JOBSDIR + '/' + 'dorothea.sh'
    jobfile     = open(jobfilename, 'w')
    jobfile.write(exec_template.format(**exec_params))

    cmd = 'python $ICDIR/cities/dorothea.py -c {}\n'.format(config_file)
    jobfile.write(cmd)
