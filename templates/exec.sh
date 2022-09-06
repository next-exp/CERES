#!/bin/bash
#PBS -N {jobname}
#PBS -q short
#PBS -o {jobout}
#PBS -e {joberr}
#PBS -M jmbenlloch@ific.uv.es

echo date
date
source /software/miniconda3_dev/etc/profile.d/conda.sh
export ICTDIR=/software/IC-v1.2.0
export ICDIR=$ICTDIR/invisible_cities
export PATH="$ICTDIR/bin:$PATH"
export PYTHONPATH=$ICTDIR:$PYTHONPATH
export OMP_NUM_THREADS=1
#conda activate IC-3.7-2018-11-14
conda activate IC-3.7-2020-06-16
