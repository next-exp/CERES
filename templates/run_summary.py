from glob import glob
from datetime import datetime, timedelta
import sys, os
import re
from math import sqrt
from functools import reduce

def events_and_time(fname):
    textfile = open(fname, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall("run (?P<nevts>\d+) evts in (?P<time>\d+\.\d+) s", filetext)
    evts_times = list(map(lambda t: (int(t[0]), float(t[1])), matches))
    total_evts = sum(map(lambda t: t[0], evts_times))
    total_time = sum(map(lambda t: t[1], evts_times))
    return total_evts, total_time

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
config = 'irene_cs_s2_2000.conf'
run_number = {run}
path = '{logs_path}'
path_out = '{path_out}'

files = glob(path + '/*irene*.o*')
files_out = glob(path_out + '/*')

times = list(map(getTime, files))
times = list(filter(lambda ts: len(ts) > 1, times))
duration = sum(map(lambda ts : (ts[1] - ts[0]).total_seconds(), times))
start_time = sorted(times, key=lambda t: t[0])[0][0]
end_time = sorted(times, key=lambda t: t[1])[-1][1]
total_files = len(files)
total_evts, total_time = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), map(events_and_time, files))
total_size = sum(map(lambda f: os.stat(f).st_size, files_out))
release = ic_tag + '-' + ceres_tag
config_url = 'https://github.com/nextic/CERES/blob/{{}}/templates/{{}}'.format(ceres_tag, config)

params = {{
    'run' : run_number,
    'start' : start_time.strftime('%Y-%m-%d %H:%M:%S'),
    'end' : end_time.strftime('%Y-%m-%d %H:%M:%S'),
    'events' : total_evts,
    'files' : total_files,
    'type' : '{datatype}',
    'duration' : int(duration),
    'event_time' : round(duration/total_evts, 2),
    'total_size' : total_size,
    'event_size' : round(total_size / total_evts, 2),
    'location' : path_out,
    'release' : release,
    'config' : config_url
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
LOCATION="{{location}}"
CONFIG_FILE1="{{config}}"
CONFIG_FILE2=""
COMMENTS=""'''

parameters_file = os.path.join('/analysis/spool/jobs/{run}/{dir}/parameters.cfg')
open (parameters_file, 'w').write(template.format(**params))
