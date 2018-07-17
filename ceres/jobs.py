from __future__ import division

from subprocess import call
from math       import ceil
from time       import sleep

import magic
import hashlib
import os
import logging
from glob import glob

from ceres import cities
from ceres import templates
from ceres import utils

def config_files_1to1(files, args, paths, versions):
    logging.info("{} input hdf5 files found in {}".format(len(files), paths.input))
    to_process = []
    #check hdf5 file are completely written
    ftype = magic.Magic()
    for f in files:
        #if file complete type would be: "Hierarchical Data Format (version 5) data"
        if ftype.from_file(f) == 'data':
            continue

        filename     = f.split('/')[-1]
        fileno = utils.get_index_from_file_name(filename)
        #filenames: '{city}_{fileno}_{run}_{ictag}_{certestag}_{configfile}.h5
        new_name = [cities.outputs[args.city],
                    fileno,
                    args.run,
                    versions.ic,
                    versions.ceres,
                    versions.config]
        filename_out = '_'.join(new_name) + '.h5'

        #if file already exists, skip
        fout = os.path.join(paths.output, filename_out)
        logging.debug("Output file: {}".format(fout))
        if os.path.isfile(fout):
            logging.info("Skipping {}".format(fout))
            continue

        params = {}
        if versions.version == 'prod':
            params['pathin']  = '.'
            params['pathout'] = '.'
        params['filein' ] = os.path.join(paths.input, filename)
        params['fileout'] = fout
        params['run']     = args.run

        template = templates.get(args.city, args.type)

        config_file = os.path.join(paths.configs, filename + '.conf')
        open (config_file, 'w').write(template.format(**params))
        logging.debug("Creating {}".format(config_file))

        to_process.append(config_file)
        if len(to_process) == float(args.maxfiles):
            logging.info("Already processed the number of files requested! Stopping at {} files"\
                         .format(args.maxfiles))
            break

    return to_process


def config_files_allto1(files, args, paths, versions):
    to_process = []
    #filenames: '{city}_{run}_{ictag}_{certestag}_{configfile}.h5
    new_name = [cities.outputs[args.city],
                args.run,
                versions.ic,
                versions.ceres,
                versions.config]
    filename_out = '_'.join(new_name) + '.h5'

    params = {}
    if versions.version == 'prod':
        params['pathin']  = '.'
        params['pathout'] = '.'
    params['filein' ] = os.path.join(paths.input, '*h5')
    params['fileout'] = os.path.join(paths.output, filename_out)
    logging.debug("Output file: {}".format(params['fileout']))
    params['run']     = args.run

    template = templates.get(args.city, args.type)

    config_file = os.path.join(paths.configs, filename_out + '.conf')
    open (config_file, 'w').write(template.format(**params))
    logging.debug("Creating {}".format(config_file))

    to_process.append(config_file)
    return to_process

def generate_configs(files, args, paths, versions):
    logging.info("Creating config files in {}".format(paths.configs))
    conf_type = cities.configs[args.city]
    config_files = []
    if conf_type == '1to1':
        config_files = config_files_1to1(files, args, paths, versions)
    if conf_type == 'allto1':
        config_files = config_files_allto1(files, args, paths, versions)
    return config_files


def generate_jobs(configs, args, paths, versions):
    if not len(configs):
        logging.warning("All files has already been processed!")
        exit(0)
    logging.info("Jobs directory: {}".format(paths.jobs))
    to_submit = []
    #Generate exec files
    template = templates.exec_template()
    exec_params = {'jobname': 'to_be_filled',
                   'jobout' : paths.logs,
                   'joberr' : paths.logs}

    #jobfile    = file

    nfiles     = int(ceil(len(configs) * 1.0 / int(args.jobs)))
    njobs = int(len(configs)/nfiles)
    logging.info("Creating {} job files, files per jobs: {}".format(njobs, nfiles))

    offset = 0
    if 'file' in args:
        print(args.file)
        offset = int(args.file)

    count_jobs = 0
    for i, config in enumerate(configs):
        if i % nfiles == 0:
            if i: # write at the end of each file
                close_job_file(jobfile, args, paths, count_jobs)

            jobfilename = '{}_{}.sh'.format(args.city, count_jobs+offset)
            jobfilename = os.path.join(paths.jobs, jobfilename)
            to_submit.append(jobfilename)
            logging.debug("Creating {}".format(jobfilename))

            job_name = '{}_{}_{}'.format(args.run, args.city, count_jobs+offset)
            exec_params['jobname'] = job_name

            jobfile     = open(jobfilename, 'w')
            jobfile.write(template.format(**exec_params))
            count_jobs += 1

        cmd = 'city {} {}\n'.format(args.city, config)
        jobfile.write(cmd)

    if not jobfile.closed:
        close_job_file(jobfile, args, paths, count_jobs)

    return to_submit

def close_job_file(jobfile, args, paths, count_jobs):
    jobfile.write('\n\necho date\ndate\n')
    analysis_number = get_analysis_number(paths.output)
    monitor_file = 'touch /analysis/spool/jobs/{}/{}/job_{}.txt\n'.format(args.run, analysis_number, count_jobs)
    jobfile.write(monitor_file)
    jobfile.close()


def submit(jobs, args):
    logging.info("Submitting {} jobs".format(len(jobs)))
    for job in jobs:
        cmd = 'qsub {}'.format(job)
        logging.debug(cmd)
        call(cmd, shell=True, executable='/bin/bash')
        sleep(0.3)

def run_summary(jobs, args, paths, versions):
    base_path = '/analysis/spool/jobs/' + args.run + '/'
    analysis_number = get_analysis_number(paths.output)
    base_path = base_path + str(analysis_number)
    if not os.path.isdir(base_path):
        os.makedirs(base_path)
    count_file = base_path + '/job_counter.txt'
    with open(count_file, 'w') as count:
        count.write(str(len(jobs)) + '\n')

    template_py, template_sh = templates.summary_template()
    params = {'ic_tag': versions.ic,
              'ceres_tag' : versions.ceres,
              'logs_path' : paths.logs,
              'path_out'  : paths.output,
              'path_in'   : paths.input,
              'config'    : templates.getTemplateFilename(args.city, args.type),
              'run' : args.run,
              'datatype' : cities.outputs[args.city].upper(),
              'city' : args.city,
              'dir' : analysis_number}

    py_file = os.path.join(base_path, 'run_summary.py')
    open (py_file, 'w').write(template_py.format(**params))

    sh_file = os.path.join(base_path, 'run_summary.sh')
    open (sh_file, 'w').write(template_sh.format(**params))


def get_analysis_number(path):
    return hashlib.md5(os.fsencode(path)).hexdigest()
