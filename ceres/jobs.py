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

        ###-------
        # filename     = f.split('/')[-1]
        # fileno = utils.get_index_from_file_name(filename)
        # #filenames: '{city}_{fileno}_{run}_[{trg1/2}]_{ictag}_{certestag}_{configfile}.h5
        # new_name = [cities.outputs[args.city],
        #             args.run,
        #             fileno,
        #             "trg",
        #             versions.ic,
        #             versions.ceres,
        #             versions.config]
        # #compute filenames and paths in case of dual mode
        # filenames_out = []
        # paths_out     = []
        # for trg in range(2):
        #     new_name[3] = "trigger{}".format(trg+1)
        #     filenames_out.append('_'.join(new_name) + '.h5')
        #     paths_out.append(os.path.join(paths.output, "trigger{}".format(trg+1)))
        # list(map(utils.check_make_dir, paths_out))

        # # compute output file names
        # fouts = []
        # for outdir, fout in zip(paths_out, filenames_out):
        #     fouts.append(os.path.join(outdir, fout))

        # # if args.trigger==2 the output file is the second one
        # if args.trigger == '2':
        #     fouts.reverse()
        ###-------

        fout = 'run_{}_{:04d}_ldc{}_trg{}.{}.{}.{}.{}.h5'.format(args.run,int(args.file),
                                                                 args.ldc,args.trigger,
                                                                 versions.ic,versions.ceres,
                                                                 versions.config,
                                                                 args.city)
        pout = os.path.join(paths.output,'trigger{}'.format(args.trigger))
        utils.check_make_dir(pout)
        
        #if file already exists, skip
        #for fout in fouts:
        logging.info("Output file: {}".format(fout))
        if os.path.isfile(os.path.join(pout,fout)):
            if(args.reprocess):
                logging.info("Reprocessing {}".format(fout))
            else:
                logging.info("Skipping {}: reprocessing not allowed".format(fout))
                continue
        
        params = {}
        if versions.version == 'prod':
            params['pathin']   = '.'
            params['pathout']  = '.'
            params['pathout2'] = '.'
        params['filein' ]  = os.path.join(paths.input, os.path.basename(f))
        params['fileout']  = os.path.join(pout,fout) #fouts[0]
        #if len(fouts) > 1:
        #    params['fileout2'] = fouts[1]
        params['run']      = args.run

        template = templates.get(args.city, args.type)

        config_file = os.path.join(paths.configs,os.path.basename(f)+'.'+(args.city)+'.conf')
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
    
    #compute filenames and paths in case of dual mode
    filenames_out = []
    paths_out     = []
    for trg in range(2):
        new_name[3] = "trigger{}".format(trg+1)
        filenames_out.append('_'.join(new_name) + '.h5')
        paths_out.append(os.path.join(paths.output, "trigger{}".format(trg+1)))
    list(map(utils.check_make_dir, paths_out))

    # compute output file names
    fouts = []
    for outdir, fout in zip(paths_out, filenames_out):
        fouts.append(os.path.join(outdir, fout))

    # if args.trigger==2 the output file is the second one
    if args.trigger == '2':
        fouts.reverse()

    params = {}
    if versions.version == 'prod':
        params['pathin']  = '.'
        params['pathout'] = '.'
    params['filein' ] = os.path.join(paths.input, '*h5')
    params['fileout']  = fouts[0]
    if len(fouts) > 1:
        params['fileout2'] = fouts[1]
    #params['fileout'] = os.path.join(paths.output, filename_out)
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
                   'jobout' : '/dev/null',
                   'joberr' : '/dev/null'}

    #jobfile    = file

    nfiles     = int(ceil(len(configs) * 1.0 / int(args.jobs)))
    njobs = int(len(configs)/nfiles)
    logging.info("Creating {} job files, files per jobs: {}".format(njobs, nfiles))

    offset = 0
    if args.file:
        offset = int(args.file)

    count_jobs = 0
    for i, config in enumerate(configs):
        if i % nfiles == 0:
            if i: # write at the end of each file
                close_job_file(jobfile, args, paths, count_jobs)

            jobfilename = '{}_{}_ldc{}_trigger{}.sh'.format(args.city,count_jobs+offset,
                                                            args.ldc,args.trigger)
            
            jobfilename = os.path.join(paths.jobs, jobfilename)
            to_submit.append(jobfilename)
            logging.debug("Creating {}".format(jobfilename))

            job_name = '{}_{}_{}'.format(args.run, args.city, count_jobs+offset)
            exec_params['jobname'] = job_name

            jobfile     = open(jobfilename, 'w')
            jobfile.write(template.format(**exec_params))
            count_jobs += 1

        log_base = "{}/{}_{}_{}_ldc{}_trigger{}".format(paths.logs, args.city, args.run,
                                                  count_jobs+offset-1, args.ldc,args.trigger)
        log_out = log_base + ".out"
        log_err = log_base + ".err"

        config_template = templates.getTemplateFilename(args.city, args.type)
        config_url = 'https://github.com/nextic/CERES/blob/{}/templates/{}'
        config_url = config_url.format(versions.ceres, config_template)
        #put config template in the log file
        cmd = 'echo config_url = {} > {}\n'.format(config_url, log_out)
        jobfile.write(cmd)
        cmd = 'city {} {} 1>>{} 2>{}\n'.format(args.city, config, log_out, log_err)
        jobfile.write(cmd)
        cmd = 'echo "job finished" >> {}\n'.format(log_out)
        jobfile.write(cmd)

    if not jobfile.closed:
        close_job_file(jobfile, args, paths, count_jobs)

    return to_submit

def close_job_file(jobfile, args, paths, count_jobs):
    jobfile.write('\n\necho date\ndate\n')
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
    utils.check_make_dir(base_path)

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
