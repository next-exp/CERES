from __future__ import division

from subprocess import call
from math       import ceil
from time       import sleep

import magic
import os
import logging

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
        new_name = [args.isotope,
                    cities.outputs[args.city],
                    fileno,
                    args.next_tag,
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
        params['filein' ] = filename
        params['fileout'] = filename_out

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


#TODO: fix for MC
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
    params['filein' ] = os.path.join(paths.input, '*h5')
    params['fileout'] = os.path.join(paths.output, filename_out)
    logging.debug("Output file: {}".format(params['fileout']))

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
    logging.info("Exec directory: {}".format(paths.execs))
    logging.info("Jobs directory: {}".format(paths.jobs))
    to_submit = []
    #Generate exec files
    template = templates.exec_template()
    exec_params = {'city'       : args.city,
                   'pathin'     : paths.input,
                   'pathout'    : paths.output,
                   'configfile' : 'to be filled',
                   'filein'     : 'to be filled',
                   'fileout'    : 'to be filled'}

    #Generate job files
    job_template = templates.job_template()

    njobs = len(configs)
    count_jobs = 0
    logging.info("Creating {} job files, files per jobs: {}".format(njobs, 1))
    for i, config in enumerate(configs):
        basename = config.split('/')[-1][:-5]
        execfilename = os.path.join(paths.execs, basename + '.sh')
        to_submit.append(execfilename)
        logging.debug("Creating {}".format(execfilename))

        exec_file     = open(execfilename, 'w')
        exec_params['configfile'] = config
        filein_pattern  = 'files_in(.*)=(.*)\'(?P<in>.+)\''
        fileout_pattern = 'file_out(.*)=(.*)\'(?P<out>.+)\''
        filein  = utils.find_pattern_in_file(filein_pattern , config ,'in')
        fileout = utils.find_pattern_in_file(fileout_pattern, config ,'out')
        exec_params['filein'] = filein
        exec_params['fileout']  = fileout
        exec_file.write(template.format(**exec_params))
        exec_file.close()

            #Job file
        out = os.path.join(paths.logs, basename + '.out')
        err = os.path.join(paths.logs, basename + '.err')
        log = os.path.join(paths.logs, basename + '.log')
        job_params = {'exec'   : execfilename,
                      'output' : out,
                      'err'    : err,
                      'log'    : log}
        jobfilename = os.path.join(paths.jobs, basename + '.submit')
        logging.debug("Creating {}".format(jobfilename))
        jobfile     = open(jobfilename, 'w')
        jobfile.write(job_template.format(**job_params))
        jobfile.close()
        to_submit.append(jobfilename)
        count_jobs += 1

    return to_submit

def submit(jobs):
    logging.info("Submitting {} jobs".format(len(jobs)))
    for job in jobs:
        cmd = 'condor_submit {}'.format(job)
        logging.debug(cmd)
        call(cmd, shell=True, executable='/bin/bash')
        sleep(0.3)

