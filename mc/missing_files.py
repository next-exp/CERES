import os
import sys
import re
from glob import glob

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

#jobs = '/lustre/ific.uv.es/sw/ific/NEXT/Releases/NEXT_v1_00_05/GridSubmit_jm/prod/Cs_7bar10000/ACTIVE/jdl'

def check_missing(jobs):
    for job in glob(jobs + '/*submit'):
        pattern = '(\s*)executable(\s*)=(\s*)(?P<exec>.*)'
        exec_file = find_pattern(pattern, job, 'exec')

#        pattern = '(\s*)city(\s*)(\w+)(\s*)(?P<path>/.*conf)'
#        config_file = find_pattern(pattern, exec_file, 'path')

        pattern = '(\s*)xrdcp(\s*)(.*)(\.h5)(.*)root://eospublic.cern.ch(?P<path>/.*h5)'
        fileout = find_pattern(pattern, exec_file, 'path')
#        print fileout

        if not os.path.isfile(fileout):
            print ("condor_submit {}".format(job))

if __name__ == '__main__':
    if len(sys.argv) > 1:
	    check_missing(sys.argv[1])
