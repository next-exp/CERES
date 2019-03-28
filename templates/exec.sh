#!/bin/bash
#PBS -N {jobname}
#PBS -q short
#PBS -o {jobout}
#PBS -e {joberr}
#PBS -M jmbenlloch@ific.uv.es

echo date
date
#export PATH="/software/miniconda3/bin:$PATH"
#export LD_LIBRARY_PATH="/software/miniconda3/lib:$LD_LIBRARY_PATH"
source /software/miniconda3/etc/profile.d/conda.sh
export ICTDIR=/software/IC
export ICDIR=$ICTDIR/invisible_cities
export PATH="$ICTDIR/bin:$PATH"
export PYTHONPATH=$ICTDIR:$PYTHONPATH
source activate IC-3.7-2018-11-14
