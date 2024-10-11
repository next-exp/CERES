#!/bin/bash
#PBS -N {jobname}
#PBS -q short
#PBS -o {jobout}
#PBS -e {joberr}
#PBS -l mem={mem}
#PBS -M jmbenlloch@ific.uv.es

echo date
date
source /data/software/miniconda/etc/profile.d/conda.sh
export ICTDIR=/data/software/IC
export ICDIR=$ICTDIR/invisible_cities
export PATH="$ICTDIR/bin:$PATH"
export PYTHONPATH=$ICTDIR:$PYTHONPATH
export OMP_NUM_THREADS=1
conda activate IC-3.8-2022-04-13
