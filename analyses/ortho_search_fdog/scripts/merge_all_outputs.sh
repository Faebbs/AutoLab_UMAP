#!/bin/bash

mkdir merged_all_output
cd merged_all_output

ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cd/output/chitin.extended.fa.gh chitin.extended.fa
ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cd/output/chitin.phyloprofile.gh.valid chitin.phyloprofile
ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cd/output/chitin_forward.domains.gh chitin_forward.domains

ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cellulase/output/merged/cellulase_all.extended.fa .
ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cellulase/output/merged/cellulase_all.phyloprofile.valid cellulase_all.phyloprofile
ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cellulase/output/merged/cellulase_all_forward.domains .

ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cbm/output/cbm.extended.fa.gh cbm.extended.fa
ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cbm/output/cbm.phyloprofile.gh.valid cbm.phyloprofile
ln -s /share/gluster/Projects/vinh/fdog_ms/usecase_cbm/output/cbm_forward.domains.gh cbm_forward.domains

fdog.mergeOutput -i . -o cell_wall
