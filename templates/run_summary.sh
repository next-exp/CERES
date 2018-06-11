#!/bin/bash
export PATH="/software/miniconda3/bin:$PATH"
export LD_LIBRARY_PATH="/software/miniconda3/lib:$LD_LIBRARY_PATH"

python /analysis/spool/jobs/{run}/{dir}/run_summary.py
