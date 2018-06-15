#output dirs for cities
outputs = {'irene'       : 'pmaps',
           'dorothea'    : 'kdst',
           'penthesilea' : 'hdst'}

# Wether to use generate one job per input file (1to1)
# or one job for all input files
configs = {'irene'       : '1to1',
           'dorothea'    : '1to1',
           'penthesilea' : '1to1'}

#input dirs for cities
inputs = {'irene'       : 'data',
          'dorothea'    : outputs['irene'],
          'penthesilea' : outputs['irene']}
