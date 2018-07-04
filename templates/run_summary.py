from glob import glob
from datetime import datetime, timedelta
import sys, os
import numpy as np
import re
from math import sqrt
from functools import reduce

def events_and_time(fname):
    textfile = open(fname, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall("run (?P<nevts>\d+) evts in (?P<time>\d+\.\d+) s", filetext)
    match_file = re.findall("Opening (?P<filename>.+)\.\.\.", filetext)
    evts_times = list(map(lambda t: (int(t[0]), float(t[1])), matches))
    total_evts = sum(map(lambda t: t[0], evts_times))
    total_time = sum(map(lambda t: t[1], evts_times))

    times = {}
    evts  = {}
    for fname, params in zip(match_file, matches):
        evts[fname] = int(matches[0][0])
        times[fname] = float(matches[0][1])

    return evts, times

def getTime(logfile):
    with open(logfile, 'r') as log:
        times = []
        flag = False
        for line in log:
            if flag:
                time_str = ' '.join(str.strip(line).split()[1:])
                time = datetime.strptime(time_str, '%b %d %H:%M:%S %Z %Y')
                times.append(time)
                flag = False
            if line == 'date\n':
                flag = True
    return times

ic_tag = '{ic_tag}'
ceres_tag = '{ceres_tag}'
config = '{config}'
run_number = {run}
path = '{logs_path}'
path_out = '{path_out}'
path_in  = '{path_in}'

files = glob(path + '/*{city}*.o*')
error_files = glob(path + '/*{city}*.e*')
files_out = glob(path_out + '/*')

error = sum(map(lambda f: os.stat(f).st_size, error_files))
output_code = 'OK' if not error else 'ERROR'

times = list(map(getTime, files))
times = list(filter(lambda ts: len(ts) > 1, times))
duration = sum(map(lambda ts : (ts[1] - ts[0]).total_seconds(), times))
start_time = sorted(times, key=lambda t: t[0])[0][0]
end_time = sorted(times, key=lambda t: t[1])[-1][1]
total_files = len(files)

evts  = {}
times = {}

for f in files:
    evts_partial, times_partial = events_and_time(f)
    evts.update(evts_partial)
    times.update(times_partial)

total_evts = sum(evts.values())
total_time = sum(times.values())

total_size = sum(map(lambda f: os.stat(f).st_size, files_out))
release = ic_tag + '-' + ceres_tag
config_url = 'https://github.com/nextic/CERES/blob/{{}}/templates/{{}}'.format(ceres_tag, config)

try:
    evt_time = round(duration/total_evts, 2)
    evt_size = round(total_size / total_evts, 2)
except:
    evt_time = 0
    evt_size = 0

params = {{
    'run' : run_number,
    'start' : start_time.strftime('%Y-%m-%d %H:%M:%S'),
    'end' : end_time.strftime('%Y-%m-%d %H:%M:%S'),
    'events' : total_evts,
    'files' : total_files,
    'type' : '{datatype}',
    'duration' : int(duration),
    'event_time' : evt_time,
    'total_size' : total_size,
    'event_size' : evt_size,
    'location' : path_out,
    'father_location' : path_in,
    'release' : release,
    'config' : config_url,
    'code' : output_code,
}}

template = '''RUN_NUMBER="{{run}}"
AUTHOR="icuser"
DATA_TYPE="DATA"
TIME_START="{{start}}"
TIME_END="{{end}}"
ANALYSIS_TYPE="{{type}}"
RELEASE_NUMBER="{{release}}"
PRODUCTION="IC"
TOTAL_EVENTS="{{events}}"
TOTAL_FILES="{{files}}"
TOTAL_SIZE="{{total_size}}"
DURATION="{{duration}}"
EVENT_TIME="{{event_time}}"
EVENT_SIZE="{{event_size}}"
FATHER_LOCATION="{{father_location}}"
LOCATION="{{location}}"
CONFIG_FILE1="{{config}}"
CONFIG_FILE2=""
OUTPUT_CODE="{{code}}"
COMMENTS=""'''

parameters_file = os.path.join('/analysis/spool/jobs/{run}/{dir}/parameters.cfg')
open (parameters_file, 'w').write(template.format(**params))
