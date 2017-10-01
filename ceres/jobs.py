import magic
import os

from ceres import cities
from ceres import templates
from ceres import utils

def config_files_1to1(files, args, paths, versions):
    to_process = []
    #check hdf5 file are completely written
    ftype = magic.Magic()
    for f in files:
        #if file complete type would be: "Hierarchical Data Format (version 5) data"
        if ftype.from_file(f) == 'data':
            continue

        filename     = f.split('/')[-1]
        fileno = utils.get_index_from_file_name(filename)
        #filenames: '{city}_{fileno}_{run}_{ictag}_{certestag}_{configfile}.h5
        new_name = [cities.outputs[args.city],
                    fileno,
                    args.run,
                    versions.ic,
                    versions.ceres,
                    versions.config]
        filename_out = '_'.join(new_name) + '.h5'
        print (filename_out)

        #if file already exists, skip
        fout = os.path.join(paths.output, filename_out)
        if os.path.isfile(fout):
            print("skip ", fout)
            continue

        params = {}
        params['filein' ] = os.path.join(paths.input, filename)
        params['fileout'] = fout
        params['run']     = args.run

        template = templates.get(args.city, args.type)

        config_file = os.path.join(paths.configs, filename + '.conf')
        print(config_file)
        open (config_file, 'w').write(template.format(**params))

        to_process.append(config_file)
        if len(to_process) == args.maxfiles:
            break

    return to_process


def config_files_allto1(files, args, paths, versions):
    to_process = []
    #filenames: '{city}_{run}_{ictag}_{certestag}_{configfile}.h5
    new_name = [cities.outputs[args.city],
                args.run,
                versions.ic,
                versions.ceres,
                versions.config]
    filename_out = '_'.join(new_name) + '.h5'
    print (filename_out)

    params = {}
    params['filein' ] = os.path.join(paths.input, '*h5')
    params['fileout'] = os.path.join(paths.output, filename_out)
    params['run']     = args.run

    template = templates.get(args.city, args.type)

    config_file = os.path.join(paths.configs, filename_out + '.conf')
    print(config_file)
    open (config_file, 'w').write(template.format(**params))

    to_process.append(config_file)
    return to_process

def generate_configs(files, args, paths, versions):
    conf_type = cities.configs[args.city]
    if conf_type == '1to1':
        config_files_1to1(files, args, paths, versions)
    if conf_type == 'allto1':
        config_files_allto1(files, args, paths, versions)

