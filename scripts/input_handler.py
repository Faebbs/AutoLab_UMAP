import argparse
import warnings

def take_input():
    """
    Takes the Arguments from function call, checks validity and returns dict containing them.
    :return: dict with arguments
    """
    # add command line arguments
    parser = argparse.ArgumentParser(prog="autoalloUMAP",
                                     description="Tool for UMAP Visualisation")  # automatic allocation umap
    required_group = parser.add_argument_group("Required arguments")
    input_group = parser.add_argument_group("Optional arguments for input data")
    plot_group = parser.add_argument_group("Optional plotting arguments")
    utility_group = parser.add_argument_group("Optional utilities")
    umap_group = parser.add_argument_group("Optional UMAP arguments")

    required_group.add_argument("--file", "-f", required=True,
                                help="Path to input file, should be CSV/TSV")
    input_group.add_argument("--sep", "-s", default="\t",
                             help="Seperator for CSV")
    required_group.add_argument("--genecolumn", "-g", required=True,
                                help="Name of the column which holds the geneIDs (from CAZy Database).")
    required_group.add_argument("--ncbiidcolumn", "-n", required=True,
                                help="Name of the column which holds the ncbiIDs.")
    required_group.add_argument("--joinon", "-jo", default=None,
                                help="Name of the column, which defines the new rows of the occurance matrix. Has to be either the column with geneIDs or ncbiIDs."
                                     " Default is the column with ncbiIDs")
    required_group.add_argument("--occurance_data", "-od", required=True, nargs="+",
                                help="Define which column(s) should be used in creating the UMAP."
                                     " Can be more than one column, if this is the case, will take the average of every row.")
    input_group.add_argument("--maskvalue", "-mask", default=None,
                             help="Filters out all nodes which have less than specified presence/absence score. Sets values that meet threshold to 1, others to 0")
    utility_group.add_argument("--updateLocalDatabase", "-ulD", action="store_true",
                               help="Decide if you want to update your local Database, should be True first time running")
    plot_group.add_argument("-port", default=8050,
                            help="Specify Port in which the Dash app should be opend. Default is 8050")
    utility_group.add_argument("--csvfile", "-csv", action="store_true",
                               help="If True, saves the data used to create the plot in a csv file in results directory")
    plot_group.add_argument("--colorscale", "-cscal", default="Rainbow",
                            help="Choose a colorscale from plotlys samplecolors."
                                 " More Info about colorscales: https://plotly.com/python/builtin-colorscales/")
    plot_group.add_argument("--opacity", "-op", default="0.6",
                            help="Set opacity for the marks in the plot. Value between 0 and 1, 1 being no opacity.")
    plot_group.add_argument("--additional_ranks", "-adr", nargs="*",
                            help="Let's you add additional ranks to search for in NCBI Lineage. Default are: Kingdom, Phylum, Class, Order, Family, Genus, Species."
                                 " Those are also the most universally used. Other ranks will probably result in a lot of unassigned marks in the plot."
                                 " Only takes effect if --joinon is containing ncbiIDs")
    utility_group.add_argument("--runtime", "-rt",
                               help="Show runtime for program", action="store_true")
    umap_group.add_argument("--n_neighbors", "-ngb", default="15",
                            help="UMAP parameter: The size of local neighborhood (in terms of number of neighboring sample points)"
                                 " used for manifold approximation. Larger values result in more global views of the manifold,"
                                 " while smaller values result in more local data being preserved. In general values should be in the range 2 to 100.")
    umap_group.add_argument("--min_dist", "-mdis", default="0.1",
                            help="UMAP parameter: The effective minimum distance between embedded points. Smaller values"
                                 " will result in a more clustered/clumped embedding where nearby points on the manifold are"
                                 " drawn closer together, while larger values will result on a more even dispersal of points."
                                 " The value should be set relative to the spread value, which determines the scale at which embedded points will be spread out.")
    umap_group.add_argument("--spread", "-sp", default="1.0",
                            help="UMAP parameter: The effective scale of embedded points. In combination with min_dist"
                                 " this determines how clustered/clumped the embedded points are.")
    umap_group.add_argument("--seed", default=None,
                            help="UMAP parameter (Altered only int as parameter): : If given int, random_state is the seed used by the random number generator."
                                 " By dooing so, UMAP will be slower because Multithreading is disabled.")
    # parse Arguments from command line
    args = parser.parse_args()

    # check Arguments and executes main
    data = args.file  # file path

    separator = args.sep  # separator in filepath
    if separator not in ["\t", ","]:
        warnings.warn("You typed in " + separator + " as a separator. Most of the time as CSV/TSV uses " + repr("\t") + " or ','. \n"
                        "If errors occur check if " + separator + " is really the the symbol used in your CSV/TSV.")

    genecolumn = args.genecolumn  # name of column with geneIDs

    ncbiidcolumn = args.ncbiidcolumn  # name of column with ncbiIDs

    join_on = args.joinon # name of the column with the info which is used as rows in occurance matrix
    if join_on is None:
        join_on = ncbiidcolumn
    else:
        if join_on != genecolumn and join_on != ncbiidcolumn:
            raise Exception("joinon parameter has to be the same as either genecolumn or ncbiidcolumn")

    occurance_data = args.occurance_data  # name of column used for data which is used by UMAP
    if len(occurance_data) < 1:
        raise Exception("Give at least 1 Column name in your data")

    maskvalue = args.maskvalue  # Value threshold
    if maskvalue is not None:
        try:
            maskvalue = float(maskvalue)
        except(ValueError, TypeError):
            raise Exception("Maskvalue has to be a float number")

    updateLocalDatabase = args.updateLocalDatabase  # update local database

    port = args.port  # port for localhost
    try:
        port = int(port)
    except(ValueError, TypeError):
        raise Exception("Port has to be a number")

    csvfile = args.csvfile  # store matrix data as csv

    colorscale = args.colorscale  # choose colorscale

    opacity = args.opacity  # choose opacity
    try:
        opacitytest = float(opacity)
        if opacitytest < 0 or opacitytest > 1:
            raise Exception("Opacity has to be a float value between 0 and 1")
    except(ValueError, TypeError):
        raise Exception("Opacity has to be a float value between 0 and 1")

    additional_ranks_raw = args.additional_ranks
    additional_ranks = []
    for el in additional_ranks_raw:
        el = el.lower()
        additional_ranks.append(el)

    track_time = args.runtime  # check runtime

    n_neighbors = args.n_neighbors  # number neighbors in UMAP
    try:
        n_neighbors = int(n_neighbors)
        if n_neighbors < 1:
            raise Exception("n_neighbors must be greater than 0")
    except(ValueError, TypeError):
        raise Exception("n_neighbors must be integer value")

    min_dist = args.min_dist  # min dist between points
    try:
        min_dist = float(min_dist)
    except(ValueError, TypeError):
        raise Exception("min_dist has to be a float value")

    spread = args.spread  # spread of points
    try:
        spread = float(spread)
    except(ValueError, TypeError):
        raise Exception("spread has to be a float value")

    seed = args.seed  # seed for reproducibility
    if seed is None:
        pass
    else:
        try:
            seed = int(seed)
        except(ValueError, TypeError):
            raise Exception("seed has to be an integer value")

    parameter_dict = {
        "file": data,
        "separator": separator,
        "genecolumn": genecolumn,
        "ncbiidcolumn": ncbiidcolumn,
        "join_on": join_on,
        "occurance_data": occurance_data,
        "maskvalue": maskvalue,
        "updateLocalDatabase": updateLocalDatabase,
        "port": port,
        "csvfile": csvfile,
        "colorscale": colorscale,
        "additional_ranks": additional_ranks,
        "opacity": opacity,
        "track_time": track_time,
        "n_neighbors": n_neighbors,
        "min_dist": min_dist,
        "spread": spread,
        "seed": seed
    }

    # print(parameter_dict)

    return(parameter_dict)
