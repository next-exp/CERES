# CERES

CERES is the repository for IC productions scripts & config files.

## Contents

[Canfranc setup](#canfranc-setup)

[Data structure](#data-structure)

[Running](#running)

[Templates](#templates)

[Testing](#testing)

## Canfranc setup <a name="canfranc-setup"></a>

There are two main branches for data processing at Canfranc: `master` & `dev`. In `master` we have the templates for the stable version of IC while in `dev` we have the corresponding versions for the dev IC installed at Canfranc.

They both work in the same way and there are two CERES installations in Canfranc:

 - `/home/icuser/CERES`: `prod` version.
 - `/home/icuser/CERES_dev`: `dev` version.

## Data structure <a name="data-structure"></a>

The file structure created will be the following:

`/analysis/4730/hdf5/{prod/dev}/{ictag}/{cerestag}/{pmaps,kdst,hdst,configs,logs,jobs}/{output_files}`

The filenames follows this patterns:

`{pmaps,kdst,hdst}_{fileno}_{run}_{ictag}_{cerestag}_{template}.h5`

Example:

`/analysis/4730/hdf5/prod/canfranc-old/20170921_3-7-g7d6d746/pmaps/pmaps_000_4730_canfranc-old_20170921_3-7-g7d6d746_kr1300.h5`

## Running <a name="running"></a>

To run it you one needs to move to the corresponding directory and then use the script 'run_ceres':

```
icuser@canfranc:~/CERES$ ./run_ceres                                    
usage: launch_jobs.py [-h] -j JOBS -c CITY -r RUN -t TYPE [-m MAXFILES] [-x]
                      [-ic IC_TAG] [-ceres CERES_TAG] [-d]
```

There are some mandatory arguments:

 - `-j`: Number of jobs files to produce
 - `-c`: City to run (irene, dorothea, penthesilea...)
 - `-r`: Run number
 - `-t`: Config file to use

And some optional arguments:

 - `-m`: Maximum number of input files to process
 - `-x`: Do not send the jobs the queue, just create all configs/jobs files
 - `-ic`: IC tag for the input files
 - `-ceres`: CERES tag for the input files
 - `-d`: Print debug information

Example:

```
icuser@canfranc:~/CERES$ ./run_ceres -j 50 -c irene -r 4730 -t kr1300 -m 2
INFO:root:You are running prod version with IC tag canfranc-old and CERES tag 20170921_3-11-g74d32d4
INFO:root:Files from /analysis/4730/hdf5/data will be processed
INFO:root:pmaps output files will be in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/pmaps/
INFO:root:Creating config files in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/configs/
INFO:root:10 input hdf5 files found in /analysis/4730/hdf5/data
INFO:root:Already processed the number of files requested! Stopping at 2 files
INFO:root:Jobs directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/
INFO:root:Creating 2 job files, files per jobs: 1
INFO:root:Submitting 2 jobs
0.canfranc
1.canfranc
INFO:root:Done
```

Same with debugging information:

```
icuser@canfranc:~/CERES$ ./run_ceres -j 50 -c irene -r 4730 -t kr1300 -m 2 -d
DEBUG:root:Input arguments: Namespace(ceres_tag=None, city='irene', debug=True, do_not_submit=False, ic_tag=None, jobs='50', maxfiles='2', run='4730', type='kr1300')
WARNING:root:You have modified files that are not included in a commit.Please do it with:
	git add <files>
	git commit -m "short description"
This are the files:
	README.md 
DEBUG:root:Versions(ic='canfranc-old', ceres='20170921_3-11-g74d32d4', config='kr1300', version='prod')
INFO:root:You are running prod version with IC tag canfranc-old and CERES tag 20170921_3-11-g74d32d4
DEBUG:root:Paths(input='/analysis/4730/hdf5/data', output='/analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/pmaps/', configs='/analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/configs/', jobs='/analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/', logs='/analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/logs/')
INFO:root:Files from /analysis/4730/hdf5/data will be processed
INFO:root:pmaps output files will be in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/pmaps/
DEBUG:root:directory already exists!: /analysis/4730/hdf5/data
DEBUG:root:creating directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/pmaps/
DEBUG:root:creating directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/configs/
DEBUG:root:creating directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/
DEBUG:root:creating directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/logs/
INFO:root:Creating config files in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/configs/
INFO:root:10 input hdf5 files found in /analysis/4730/hdf5/data
DEBUG:root:Output file: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/pmaps/pmaps_000_4730_canfranc-old_20170921_3-11-g74d32d4_kr1300.h5
DEBUG:root:Creating /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/configs/dst_waves.gdcsnext.000_4730.root.h5.conf
DEBUG:root:Output file: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/pmaps/pmaps_001_4730_canfranc-old_20170921_3-11-g74d32d4_kr1300.h5
DEBUG:root:Creating /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/configs/dst_waves.gdcsnext.001_4730.root.h5.conf
INFO:root:Already processed the number of files requested! Stopping at 2 files
INFO:root:Jobs directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/
INFO:root:Creating 2 job files, files per jobs: 1
DEBUG:root:Creating /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/irene_0.sh
DEBUG:root:Creating /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/irene_1.sh
INFO:root:Submitting 2 jobs
DEBUG:root:qsub /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/irene_0.sh
0.canfranc
DEBUG:root:qsub /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/irene_1.sh
1.canfranc
INFO:root:Done
```

The input files are found in the following way:

 - `irene`: There is always just one version of the input files for irene in `/analysis/{run}/hdf5/data`
 - `dorothea, penthesilea`: CERES will search for the files in `/analysis/{run}/hdf5/{prod/dev}` (depending on the version you are running). Then, if there is only one possible combination (just one IC tag and one CERES tag for the pmaps in a given run), it will use those files. 

 ```
icuser@canfranc:~/CERES$ ./run_ceres -j 50 -c dorothea -r 4730 -t kr
INFO:root:You are running prod version with IC tag canfranc-old and CERES tag 20170921_3-11-g74d32d4
INFO:root:Files from /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/pmaps will be processed
INFO:root:kdst output files will be in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/kdst/
INFO:root:Creating config files in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/configs/
INFO:root:Jobs directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-11-g74d32d4/jobs/
INFO:root:Creating 1 job files, files per jobs: 1
INFO:root:Submitting 1 jobs
2.canfranc
INFO:root:Done
 ```

 If there are more options, it won't do anything and the user will need to explicitly say which one to use:

```
icuser@canfranc:~/CERES$ ./run_ceres -j 50 -c dorothea -r 4730 -t kr
INFO:root:You are running prod version with IC tag canfranc-old and CERES tag 20170921_3-8-g8672614
ERROR:root:Cannot decide which input files version to use...
Please choose an CERES version for the input files using -ceres option:
              ['20170921_3-8-g8672614', '20170921_3-7-g7d6d746']
```

```
icuser@canfranc:~/CERES$ ./run_ceres -j 50 -c dorothea -r 4730 -t kr -ceres 20170921_3-8-g8672614
INFO:root:You are running prod version with IC tag canfranc-old and CERES tag 20170921_3-8-g8672614
INFO:root:Files from /analysis/4730/hdf5/prod/canfranc-old/20170921_3-8-g8672614/pmaps will be processed
INFO:root:kdst output files will be in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-8-g8672614/kdst/
INFO:root:Creating config files in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-8-g8672614/configs/
INFO:root:Jobs directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-8-g8672614/jobs/
INFO:root:Creating 1 job files, files per jobs: 1
INFO:root:Submitting 1 jobs
6.canfranc
INFO:root:Done
```

## Templates <a name="templates"></a>

The templates are located inside the `templates` folder. Each of them have to be also added to a dictionary in `ceres/templates.py`

```
templates = {
    'irene' : {
        'kr1300'    : 'irene_kr_s2_1300.conf'    ,
        'na_s1'     : 'irene_na_s1.conf'         ,
        'th2000'    : 'irene_th_s2_2000.conf'    ,
        'bg2000'    : 'irene_bg_s2_2000.conf'    ,
    },
    'dorothea' : {
        'kr'        : 'dorothea_kr.conf',
        'na_s1'     : 'dorothea_na.conf',
        'cs2000'    : 'dorothea_cs.conf',
        'th2000'    : 'dorothea_th.conf',
    },
    'penthesilea' : {
        'bg2000'    : 'penthesilea_bg.conf'
    }
}
```

After **EACH** change in the repository (template updates included) a commit should be done and a tag created. If not, the script will complain, but will continue working:

```
icuser@canfranc:~/CERES$ ./run_ceres -j 50 -c dorothea -r 4730 -t kr -ceres 20170921_3-8-g8672614
WARNING:root:You have modified files that are not included in a commit.Please do it with:
	git add <files>
	git commit -m "short description"
This are the files:
	run_ceres 
INFO:root:You are running prod version with IC tag canfranc-old and CERES tag 20170921_3-8-g8672614
INFO:root:Files from /analysis/4730/hdf5/prod/canfranc-old/20170921_3-8-g8672614/pmaps will be processed
INFO:root:kdst output files will be in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-8-g8672614/kdst/
INFO:root:Creating config files in /analysis/4730/hdf5/prod/canfranc-old/20170921_3-8-g8672614/configs/
INFO:root:Jobs directory: /analysis/4730/hdf5/prod/canfranc-old/20170921_3-8-g8672614/jobs/
INFO:root:Creating 1 job files, files per jobs: 1
INFO:root:Submitting 1 jobs
7.canfranc
INFO:root:Done
```

To do all that with git this is the procedure:
 ```
 git add <files>
 git commit -m "description"
 git tag <tagname>
 git push origin <tagname>
 ``` 
In principle the tag names chosen are dates like: `20171005`

## Testing <a name="testing"></a>

In the future, we will have a testing system for CERES, not ready yet, but there some sort of working prototype as you can see in (https://github.com/jmbenlloch/Canfranc), example in (https://travis-ci.org/jmbenlloch/Canfranc/builds/283491788)

