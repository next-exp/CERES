#!/bin/bash
echo date
date

# Set paths
export ICTDIR=/afs/cern.ch/work/j/jobenllo/software/IC
export ICDIR=$ICTDIR/invisible_cities
export CONDA=/afs/cern.ch/work/j/jobenllo/software/miniconda
export PATH=$CONDA/bin:$PATH
export PATH=$ICTDIR/bin:$PATH
export LD_LIBRARY_PATH=$CONDA/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ICTDIR:$PYTHONPATH
source activate IC3.6

# Copy file
xrdcp root://eospublic.cern.ch/{pathin}/{filein} {filein}
echo date
date

city {city} {configfile}
echo date
date

xrdcp {fileout} root://eospublic.cern.ch/{pathout}/{fileout}
echo date
date

# To avoid copy from condor to AFS dir
rm *h5
