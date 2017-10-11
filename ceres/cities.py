#output dirs for cities
outputs = {'diomira'     : 'rwf',
           'irene'       : 'pmaps',
           'dorothea'    : 'kdst',
           'penthesilea' : 'hdst'}

# Wether to use generate one job per input file (1to1)
# or one job for all input files
configs = {'diomira'     : '1to1',
           'irene'       : '1to1',
           'dorothea'    : 'allto1',
           'penthesilea' : '1to1'}

#input dirs for cities
inputs = {'diomira'     : 'mcrd',
          'irene'       : outputs['diomira'],
          'dorothea'    : outputs['irene'],
          'penthesilea' : outputs['irene']}
