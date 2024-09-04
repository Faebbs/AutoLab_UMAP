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
    parser = argparse.ArgumentParser(description='')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-m', '--mapping', help='Mapping file', action='store', default='', required=True)
    required.add_argument('-i', '--input', help='Domain file', action='store', default='', required=True)

    args = parser.parse_args()

    id_dict = {}
    for i in read_file(args.mapping):
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

    with open(f'{args.input}.gh', 'w') as out:
        for line in read_file(args.input):
            if not line.startswith('#'):
                id = line.split('#')[0]
                if id in id_dict:
                    new_line = line.replace(f"{id}#", f"{id_dict[id]}#")
                    new_line = new_line.replace(f"{id}|", f"{id_dict[id]}|")
                else:
                    print(f'{id}')
                    new_line = line
                out.write('%s\n' % (new_line))
            else:
                out.write('%s\n' % (line))
    print(f"DONE! Output {args.input}.gh")

if __name__ == '__main__':
    main()
