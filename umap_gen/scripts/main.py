import time
import pandas as pd
import Matrix_handler
import umap_generator
import argparse
import ncbi_data_handler


def main(file, separator, rowvalue, columnvalue, occurance_data, maskvalue,
         updateLocalDatabase, port, csvfile, colorscale, opacity, track_time,
         n_neighbors, min_dist, spread, seed):
    if track_time is True:
        start_all = time.time()
    # updates local ncbi Database
    if updateLocalDatabase is True:
        ncbi_data_handler.update_local_ncbi()
    # file path input
    try:
        data_read = pd.read_csv(file, sep=separator)
    except(FileNotFoundError):
        print("File could not be found")
        return

    # create Matrix of genes and if they appear in the organisms
    matrix = Matrix_handler.Matrix_ncbiID(data_read)
    matrix.create_matrix(rowvalue, columnvalue, occurance_data, maskvalue, track_time) #TODO Fehlerbehandlung


    # generates matrix with lineage of all ncbiIDs
    bad_IDs = []
    missng_IDs = []
    ncbiID_matrix = pd.DataFrame()
    start = time.time()
    for ncbiID in matrix.matrix_out.axes[0].tolist():
        # get lineage of organism
        func_call = ncbi_data_handler.ncbi_lineage(ncbiID)
        if func_call == "Parse Error": # If ID couldn't be parsed
            bad_IDs.append(ncbiID)
            continue
        elif func_call == "Database Error": # If ID couldn't be found in Database
            missng_IDs.append(ncbiID)
            continue
        # joins lineage on DataFrame of all organism
        df_ncbi_lineage = pd.DataFrame.from_dict(func_call, orient="index")
        new_df = pd.DataFrame({"Rank": df_ncbi_lineage.axes[0] , ncbiID: df_ncbi_lineage[0].values})
        new_df.set_index("Rank", inplace=True)
        ncbiID_matrix = ncbiID_matrix.join(new_df, how="outer")
    # caught errors display
    if len(bad_IDs) > 0:
        print(f"{len(bad_IDs)} IDs could not be parsed to Integer and therefore could not be found in database")
        out = ""
        for el in bad_IDs:
            out = out + el + ", "
        out = out[:-2]
        print(f"{out}")
        print()
    if len(missng_IDs) > 0:
        print(f"{len(missng_IDs)} IDs could not be found in Database")
        out = ""
        for el in missng_IDs:
            out = out + el + ", "
        out = out[:-2]
        print(f"{out}")
        print()
    # Tracks time if wanted
    if track_time is True:
        end = time.time()
        print(f"lineage: {end - start}s")
        end_all = time.time()
        print(f"Total runtime: {end_all-start_all}s")

    # generate UMAP
    umap_generator.generate_umap(matrix.matrix_out, ncbiID_matrix, csvfile, port, colorscale, opacity, n_neighbors, min_dist, spread, seed)





# Test data
# data = "/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile"

# main function
if __name__=="__main__":
    # add command line arguments
    parser = argparse.ArgumentParser(prog="autoalloUMAP", description="Tool for UMAP Visualisation") # automatic allocation umap
    required_group = parser.add_argument_group("Required arguments")
    input_group = parser.add_argument_group("Optional arguments for input data")
    plot_group = parser.add_argument_group("Optional plotting arguments")
    utility_group = parser.add_argument_group("Optional utilies")
    umap_group = parser.add_argument_group("Optional UMAP arguments")

    required_group.add_argument("--file", "-f", required=True,
                        help="Path to input file, should be CSV/TSV")
    input_group.add_argument("--sep", "-s", default="\t",
                        help="Seperator for CSV")
    required_group.add_argument("--rowvalue", "-r", required=True,
                        help="Define which column should be used as new row values. Relevant for NCBI Taxonomy utilisation.")
    required_group.add_argument("--columnvalue", "-c", required=True,
                        help="Define which column should be used as new column values.")
    required_group.add_argument("--occurance_data", "-od", required=True, nargs="+",
                        help="Define which column(s) should be used in creating the UMAP."
                             " Can be more than one column, if this is the case, will take the average of every row.")
    input_group.add_argument("--maskvalue", "-mask", default=None,
                        help="Filters out all nodes which have less than specified value. Sets values that meet threshold to 1, others to 0")
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
    data = args.file # file path
    # TODO Fehlerbehandlung

    seperator = args.sep # seperator in filepath
    # TODO Fehlerbehandlung

    rowvalue = args.rowvalue # name of column used for making new rows
    # TODO Fehlerbehandlung

    columnvalue = args.columnvalue # name of column used for making new columns
    # TODO Fehlerbehandlung

    occurance_data = args.occurance_data # name of column used for data which is used by UMAP
    if len(occurance_data) < 1:
        raise Exception("Give at least 1 Column name in your data")


    maskvalue = args.maskvalue # Value threshold
    if maskvalue is not None:
        try:
            maskvalue = float(maskvalue)
        except(ValueError, TypeError):
            raise Exception("Maskvalue has to be a float number")

    updateLocalDatabase = args.updateLocalDatabase # update local database

    port = args.port # port for localhost
    try:
        port = int(port)
    except(ValueError, TypeError):
        raise Exception("Port has to be a number")

    csvfile = args.csvfile # store matrix data as csv

    colorscale = args.colorscale # choose colorscale

    opacity = args.opacity # choose opacity
    try:
        opacitytest = float(opacity)
        if opacitytest < 0 or opacitytest > 1:
            raise Exception("Opacity has to be a float value between 0 and 1")
    except(ValueError, TypeError):
        raise Exception("Opacity has to be a float value between 0 and 1")

    track_time = args.runtime # check runtime

    n_neighbors = args.n_neighbors # number neighbors in UMAP
    try:
        n_neighbors = int(n_neighbors)
        if n_neighbors < 1:
            raise Exception("n_neighbors must be greater than 0")
    except(ValueError, TypeError):
        raise Exception("n_neighbors must be integer value")

    min_dist = args.min_dist # min dist between points
    try:
        min_dist = float(min_dist)
    except(ValueError, TypeError):
        raise Exception("min_dist has to be a float value")

    spread = args.spread # spread of points
    try:
        spread = float(spread)
    except(ValueError, TypeError):
        raise Exception("spread has to be a float value")

    seed = args.seed # seed for reproducibility
    if seed is None:
        pass
    else:
        try:
            seed = int(seed)
        except(ValueError, TypeError):
            raise Exception("seed has to be an integer value")

    """print(
        "data: " + str(data) + "\n" +
        "seperator: " + str(seperator) + "\n" +
        "rowvalue: " + str(rowvalue) + "\n" +
        "columnvalue: " + str(columnvalue) + "\n" +
        "transformdata: " + str(transformdata) + "\n" +
        "maskvalue: " + str(maskvalue) + "\n" +
        "updateLocalDatabase: " + str(updateLocalDatabase) + "\n" +
        "port: " + str(port) + "\n" +
        "csvfile: " + str(csvfile) + "\n" +
        "colorscale: " + str(colorscale) + "\n" +
        "opacity: " + str(opacity) + "\n" +
        "track_time: " + str(track_time) + "\n" +
        "n_neighbors: " + str(n_neighbors) + "\n" +
        "min_dist: " + str(min_dist) + "\n" +
        "spread: " + str(spread) + "\n" +
        "seed: " + str(seed)
    )"""
    
    main(data, seperator, rowvalue, columnvalue, occurance_data, maskvalue, updateLocalDatabase, port, csvfile,
         colorscale, opacity, track_time, n_neighbors, min_dist, spread, seed)

# python main.py -f /home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile -r ncbiID -c geneID -td FAS_F -mask 0.5
# python main.py -f /home/fabian/Documents/data/eukaryots.phyloprofile -r ncbiID -c geneID -od FAS_F -rt --seed 42
