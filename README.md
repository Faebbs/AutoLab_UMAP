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
Go into you're cloned repository and then execute the command with the following required and optional arguments:
```
python autoalloUMAP.py [-h] --file FILE --genecolumn GENECOLUMN --ncbiidcolumn NCBIIDCOLUMN --occurance_data OCCURANCE_DATA [OCCURANCE_DATA ...] 
                       [--sep SEP] [--maskvalue MASKVALUE] 
                       [-port PORT] [--colorscale COLORSCALE] [--opacity OPACITY] [--additional_ranks [ADDITIONAL_RANKS ...]]
                       [--joinon JOINON] [--updateLocalDatabase] [--csvfile] [--runtime] 
                       [--n_neighbors N_NEIGHBORS] [--min_dist MIN_DIST] [--spread SPREAD] [-seed SEED]
```
Close program by pressing STRG + C in the shell

___Required arguments:___
```
--file -f               Absolute path to CSV/TSV file containing phylogenetic profile 
                        (Requires a presence/absence score containg number between 0 and 1, 0:not present in organism, 1:present in organism)
--genecolumn -g         Name of the column in file which contains the genes (in CAZy Database format)
--ncbiidcolumn -n       Name of the column in file which contains the ncbiIDs
--occurance_data -od    Name of the column in file which conatins the presence/absence score. Can be more than one column, if this is the case, will take the average of every row.
                        Input like: x, y, z, ...
```

___Optional input arguments___:
```
--sep -s                Seperator for CSV/TSV file; Default=\t (TAB)
--maskvalue -mask       Threshold value for presence/absence score. If given, set value to 1 if score is above threshold; Default=None
```

___Optional plotting arguments___:
```
-port                      Port for dash app; Default=8050
--colorscale -cscal        Choose a colorscale from plotlys samplecolors; Default=Rainbow
                           More Info about colorscales: https://plotly.com/python/builtin-colorscales/
--opacity -op              Set opacity for the marks in the plot. Value between 0 and 1, 1 being no opacity; Default=0.6
--additional_ranks -adr    Let's you add additional ranks to search for in NCBI Lineage; Default=Kingdom, Phylum, Class, Order, Family, Genus, Species.
                           Those are also the most universally used. Other ranks will probably result in a lot of unassigned marks in the plot.
                           Only takes effect if --joinon is containing ncbiIDs
                           Input like: x, y, z, ...
```

___Optional utilitys___:
```
--joinon -jo            Name of the column in file which defines the new rows of the occurance matrix. Has to be either the column with geneIDs or ncbiIDs. Default=<column with ncbiIDs>
--updateLocalDatabase -ulD    Decide if you want to update your local Database. Will still update if argument is not given, but no local database is found.
--csvfile -csv                If argument is given, saves the data used to create the plot in a csv file in results directory
--runtime -rt                 Show runtime for program
```

___Optional UMAP Arguments___:
```
--n_neighbors -ngb      UMAP parameter: The size of local neighborhood (in terms of number of neighboring sample points)
                        used for manifold approximation. Larger values result in more global views of the manifold,
                        while smaller values result in more local data being preserved. In general values should be in the range 2 to 100.
                        Default=15
--min_dist -mdis        UMAP  parameter: The effective minimum distance between embedded points. Smaller values
                        will result in a more clustered/clumped embedding where nearby points on the manifold are
                        drawn closer together, while larger values will result on a more even dispersal of points.
                        The value should be set relative to the spread value, which determines the scale at which embedded points will be spread out.
                        Default=0.1
--spread -sp            UMAP parameter: The effective scale of embedded points. In combination with min_dist
                        this determines how clustered/clumped the embedded points are.
                        Default=1.0
-seed                   UMAP parameter (Altered only int as parameter): : If given int, random_state is the seed used by the random number generator.
                        By dooing so, UMAP will be slower because Multithreading is disabled.
                        Default=None
```

## Example
![example data screenshot]()


## Requirements/Dependencies
___Conda Channels:___
* conda-forge

___Packages:___
* ete3=3.1.3 (To avoid dependencies conflicts I highly recommend to start with ete3 package and download it from conda channel forge not etetoolkit channel)
* python=3.12.3
* pandas=2.2.3
* numpy=1.26.4
* requests=2.32.3
* plotly=5.24.1
* dash=2.14.2
* dash-bootstrap-components=1.6.0
* umap-learn=0.5.7


## Authors

* Fabian Mueller
