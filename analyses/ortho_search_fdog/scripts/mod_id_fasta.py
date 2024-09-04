import sys
import os
from pathlib import Path
import argparse
from Bio import SeqIO

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
    parser.add_argument('-i', '--input', help='Fasta file', action='store', default='', required = True)

    ### get arguments
    args = parser.parse_args()

    mapping_file = args.mapping
    fa_file = args.input

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

    fa_seq = SeqIO.parse(open(fa_file),'fasta')
    with open(f'{fa_file}.gh', 'w') as out:
        for fa in fa_seq:
            id = fa.id.split('|')[0]
            if id in id_dict:
                gh_id_tmp = id_dict[id].split('_')
                gh_id_mod = '_'.join(gh_id_tmp[:len(gh_id_tmp)-1])
                new_id = f"{gh_id_mod}_{fa.id}"
            else:
                new_id = fa.id
            out.write('>%s\n%s\n' % (new_id, fa.seq))

    print(f"DONE! Check output {fa_file}.gh")

if __name__ == '__main__':
    main()
