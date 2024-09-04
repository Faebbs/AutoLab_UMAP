# Data

- *coreTaxa_dir*, *searchTaxa_dir* and *annotation_dir* contain data for 18.648 refseq taxa used for the ortholog search. They originally located `/share/gluster/GeneSets/NCBI-Genomes/`. List of the taxa in each folder can be found in the corresponding *.txt* file

- The seed proteins can be found in the *seed_genes* folder under the subfolder of their corresponding reference species (the species from which the sequences was taken)

- *invalid_taxids.txt* contains either outdated or invalid taxonomy IDs that cannot be found in the taxonomy DB of PhyloProfile (March 2024)

- *id_mapping.txt* maps the seed protein IDs with their enzyme family (e.g. GH75_UKZ55717.1 means protein UKZ55717.1 belongs to GH75 family). This file is used to link the seed IDs with their enzyme family using the scripts in *scripts* folder
