import time

import pandas as pd
import argparse

from numpy.f2py.auxfuncs import throw_error

import Matrix_handler
import umap_generator
import ncbi_data_handler


def main(file, separator, rowvalue, columnvalue, transformdata, maskvalue,
         updateLocalDatabase, port, csvfile, colorscale, track_time):
    if track_time is True:
        start_all = time.time()
    # updates local ncbi Database
    if updateLocalDatabase is True:
        ncbi_data_handler.update_local_ncbi()
    # file path input
    try:
        data_read = pd.read_csv(file, sep=separator)
    except (FileNotFoundError):
        print("File could not be found")
        return

    # create Matrix of genes and if they appear in the organisms
    matrix = Matrix_handler.Matrix_ncbiID(data_read)
    matrix.create_matrix(rowvalue, columnvalue, transformdata, maskvalue, track_time) #TODO Fehlerbehandlung


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
    umap_generator.generate_umap(matrix.matrix_out, ncbiID_matrix, csvfile, port, colorscale)





# Test data
# data = "/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile"

# main function
if __name__=="__main__":
    # parsing args from command line
    parser = argparse.ArgumentParser(prog="umapvis", description="Tool for UMAP Visualisation")
    parser.add_argument("--file", "-f", help="Path to input file, should be CSV/TSV")
    parser.add_argument("--sep", "-s", help="Seperator for CSV", nargs="?")
    parser.set_defaults(sep="\t")
    parser.add_argument("--rowvalue", "-r", help="Define which column should be used as new row values. Relevant for NCBI Taxonomy utilisation.")
    parser.add_argument("--columnvalue", "-c", help="Define which column should be used as new column values.")
    parser.add_argument("--transformdata", "-td", help="Column of data which should be used for UMAP dimension reduction")
    parser.add_argument("--maskvalue", "-mv", help="Filters out all nodes which have less than specified value. 0 to get all data.")
    parser.set_defaults(maskvalue=0)
    parser.add_argument("--updateLocalDatabase", "-ulD",
                        help="Decide if you want to update your local Database, must be True first time running", nargs="?")
    parser.set_defaults(updateLocalDatabase=False)
    parser.add_argument("-port", help="Specify Port in which the Dash app should be opend. Default is 8050")
    parser.set_defaults(port=8050)
    parser.add_argument("--csvfile", "-csv", help="If True, saves the data used to create the plot in a csv file in results directory")
    parser.set_defaults(csvfile=False)
    parser.add_argument("--colorscale", "-cscal", help="Choose a colorscale from plotlys samplecolors. Default = Rainbow. More Info about colorscales: https://plotly.com/python/builtin-colorscales/")
    parser.set_defaults(colorscale="Rainbow")
    parser.add_argument("--runtime", "-rt", help="Show runtime for program")
    parser.set_defaults(runtime=False)

    args = parser.parse_args()
    data = args.file
    seperator = args.sep
    rowvalue = args.rowvalue
    columnvalue = args.columnvalue
    transformdata = args.transformdata
    maskvalue = args.maskvalue
    try:
        maskvalue = float(maskvalue)
    except(ValueError, TypeError):
        print("maskvalue has to be a number")
    updateLocalDatabase = args.updateLocalDatabase
    port = args.port
    try:
        port = int(port)
    except(ValueError, TypeError):
        print("port has to be a number")
    csvfile = args.csvfile
    if csvfile == "True":
        csvfile = True
    elif csvfile == "False":
        csvfile = False
    elif csvfile is True or csvfile is False:
        pass
    else:
        raise Exception("Value has to be either true or False")
    colorscale = args.colorscale
    track_time = args.runtime
    #TODO Fehlerbehandlung
    print(args)

    main(data, seperator, rowvalue, columnvalue, transformdata, maskvalue, updateLocalDatabase, port, csvfile, colorscale, track_time)
    print("")

# python main.py -f /home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile -r ncbiID -c geneID -td FAS_F -port 8070 -mv 0.5
