#output dirs for cities
outputs = {'hypathia'    : 'irene', # testing/debugging with MC
           'irene'       : 'irene',
           'dorothea'    : 'dorothea',
           'sophronia' : 'sophronia',
           'esmeralda'   : 'esmeralda'}

# Wether to use generate one job per input file (1to1)
# or one job for all input files
configs = {'hypathia'    : '1to1', # testing/debugging with MC
           'irene'       : '1to1',
           'dorothea'    : '1to1',
           'sophronia' : '1to1',
           'esmeralda'   : 'allto1'}

#input dirs for cities
inputs = {'hypathia'       : 'data', # testing/debugging with MC
          'irene'       : 'data',
          'dorothea'    : outputs['irene'],
          'sophronia' : outputs['irene'],
          'esmeralda' : outputs['sophronia']}
