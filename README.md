# AutoLan_UMAP

The objective of __AutoLan_UMAP__ is to simplify the visual interpretation of a phylogenetic profile. \
To achieve this it utilizes [*Uniform Manifold Approximation and Projection for Dimension Reduction (UMAP)*](https://umap-learn.readthedocs.io/en/latest/) to represent the data in a 2-dimensional space.
It also categorizes the data points by taxonomic rank via the help of [*NCBI Taxonomy Database*](https://www.ncbi.nlm.nih.gov/taxonomy).

## Table of content
* [Installation](#installation)
* [How to use](#how-to-use)
* [Requierments](#requirementsdependencies)

## Installation
1. Clone this GitHub directory to a local repository.
2. Create a Virtual Conda environment ([Link to documentation](https://docs.conda.io/projects/conda/en/latest/index.html)) from the environment.yml 
``conda env create --file environment.yml`` \
   or download [dependencies](#requirementsdependencies) manually (not recommended)

## How to use
___Required Arguments:___
```
--file -f         Path to file containing phylogenetic profile. (Requires a score)
```

## Requirements/Dependencies
___Conda Channels:___
* conda-forge
* etetoolkit

___Packages:___
* ete3=3.1.3 (To avoid dependencies conflicts I highly recommend to start with ete3 package first)
* python=3.12.2
* pandas=2.2.3
* numpy=2.0.2
* requests=2.32.3
* plotly=5.24.1
* dash=2.14.2
* dash-bootstrap-components=1.6.0
* umap-learn=0.5.7


## Authors

* Fabian Mueller
