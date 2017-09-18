#!/bin/bash
#PBS -N {jobsdir}
#PBS -q short
#PBS -o {jobsdir}
#PBS -e {jobsdir}
#PBS -M jmbenlloch@ific.uv.es

echo date
date
export PATH="/home/icuser/anaconda2/bin:$PATH"
export LD_LIBRARY_PATH="/home/icuser/anaconda2/lib:$LD_LIBRARY_PATH"
export ICTDIR=/home/icuser/IC
export ICDIR=$ICTDIR/invisible_cities
export PYTHONPATH=$ICTDIR:$PYTHONPATH
source activate IC3.5
