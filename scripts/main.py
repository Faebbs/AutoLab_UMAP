import time
import pandas as pd
from scripts import ncbi_data_handler
from scripts import umap_generator
from scripts import Matrix_handler

from scripts.input_handler import take_input


def main():
    # take input
    parameter_dict = take_input()
    file = parameter_dict["file"]
    separator = parameter_dict["separator"]
    rowvalue = parameter_dict["rowvalue"]
    columnvalue = parameter_dict["columnvalue"]
    occurance_data = parameter_dict["occurance_data"]
    maskvalue = parameter_dict["maskvalue"]
    updateLocalDatabase = parameter_dict["updateLocalDatabase"]
    port = parameter_dict["port"]
    csvfile = parameter_dict["csvfile"]
    colorscale = parameter_dict["colorscale"]
    opacity = parameter_dict["opacity"]
    track_time = parameter_dict["track_time"]
    n_neighbors = parameter_dict["n_neighbors"]
    min_dist = parameter_dict["min_dist"]
    spread = parameter_dict["spread"]
    seed = parameter_dict["seed"]

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
    main()
