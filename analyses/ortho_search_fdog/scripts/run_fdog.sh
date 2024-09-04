#!/bin/bash
#SBATCH --partition=special,inteli7,all
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=12G
#SBATCH --job-name="rhiso"
#SBATCH --array=1-212%30

srun hostname
seed=$(awk FNR==$SLURM_ARRAY_TASK_ID "/share/project/vinh/test/fdog/fdog_run/rhiso/seeds.txt")

datapath="/share/gluster/Projects/vinh/cell_wall/analyses/ortho_search_fdog/data"
seedDir="/share/gluster/Projects/vinh/cell_wall/analyses/ortho_search_fdog/data/seed_genes/RHISO@456999@016906535_1"
featureFile="/share/gluster/Projects/vinh/fdog_ms/usecase_cellulase/annoTools.txt"

outpath="/share/gluster/Projects/vinh/fdog_run/rhiso"
refspec="RHISO@456999@016906535_1"

echo $seed

time fdog.run --seqFile $seedDir/$seed.fa --jobName $seed --refspec $refspec --maxDist phylum --corepath $datapath/coreTaxa_dir --searchpath $datapath/searchTaxa_dir --annopath $datapath/annotation_dir --featureFile $featureFile  --outpath $outpath --cpus 16 --notAddingTaxa
