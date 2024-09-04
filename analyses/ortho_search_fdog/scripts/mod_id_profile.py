import sys
import os
from pathlib import Path
import argparse

def check_file_exist(file):
    """ Exit if a file does not exist"""
    if not os.path.exists(os.path.abspath(file)):
        sys.exit('%s not found' % file)


def read_file(file):
    """ Read a file and return list of lines"""
    if os.path.exists(file):
        with open(file, 'r') as f:
            lines = f.read().splitlines()
            f.close()
            return(lines)
    else:
        sys.exit('%s not found' % file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mapping', help='Mapping file', action='store', default='', required = True)
    parser.add_argument('-i', '--input', help='PhyloProfile input file', action='store', default='', required = True)

    ### get arguments
    args = parser.parse_args()

    mapping_file = args.mapping
    pp_file = args.input

    id_dict = {}
    for i in read_file(mapping_file):
        tmp = i.split('_')
        if len(tmp) == 4:
            del tmp[0]
            del tmp[0]
        if len(tmp) == 3:
            if tmp[1] == "XP":
                del tmp[0]
            else:
                del tmp[0]
                del tmp[0]
        id = '_'.join(tmp)
        id_dict[id] = i

    with open(f'{pp_file}.gh', 'w') as out:
        for line in read_file(pp_file):
            id = line.split()[0]
            if id in id_dict:
                new_line = line.replace(f"{id}\t", f"{id_dict[id]}\t")
                new_line = new_line.replace(f"{id}|", f"{id_dict[id]}|")
            else:
                print(f'{id}')
                new_line = line
            out.write('%s\n' % (new_line))

    print(f"DONE! Check output {pp_file}.gh")

if __name__ == '__main__':
    main()
