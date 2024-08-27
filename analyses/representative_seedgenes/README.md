# representative_seedgenes

For each group of paralogous seedgenes, check if they are the result of a gene duplication in Fungi. If so, select one representative that maximizes the number of orthologs in the Metazoa. Hemi-cellulase and Cellulase seedgenes were subsequently manually filtered by Ingo.

## How to use

If you create a new conda environment for this analysis. Please remember save
your environment to a file after each change:

`mamba env export > environment.yml`

You can install the python package in this directory to your local conda environment with:

`pip install -e .`

You will need to manually add large data files to .gitignore to prevent it from syncing to
version control.