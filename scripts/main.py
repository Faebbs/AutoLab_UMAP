import time
import pandas as pd
import warnings
from scripts import ncbi_data_handler
from scripts import umap_generator
from scripts import Matrix_handler
from scripts.gene_family_handler import gene_annotation

from scripts.input_handler import take_input


def main():
    # take input
    parameter_dict = take_input()
    file = parameter_dict["file"]
    separator = parameter_dict["separator"]
    genecolumn = parameter_dict["genecolumn"]
    ncbiidcolumn = parameter_dict["ncbiidcolumn"]
    join_on = parameter_dict["join_on"]
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

    # rank terms used
    list_lineage_order = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
    additional_ranks = parameter_dict["additional_ranks"]
    for el in additional_ranks:
        list_lineage_order.append(el)

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
    # check if the ncbiidcolumn and genecolumn actually exist
    column_names = list(data_read.columns)
    if ncbiidcolumn not in column_names:
        raise Exception(f"{ncbiidcolumn} is not a column name in given data")
    if genecolumn not in column_names:
        raise Exception(f"{genecolumn} is not a column name in given data")

    # create Matrix of genes and if they appear in the organisms
    matrix = Matrix_handler.Matrix_ncbiID(data_read)
    matrix.create_matrix(genecolumn, ncbiidcolumn, join_on, occurance_data, maskvalue, track_time) #TODO Fehlerbehandlung

    # generates matrix with lineage of all ncbiIDs
    bad_IDs = []
    missng_IDs = []
    ncbiID_matrix = pd.DataFrame()
    start = time.time()
    # figures out which axes (lines or columns) holds the ncbiIDs
    if join_on == ncbiidcolumn:
        axes_with_ncbiID = list(matrix.matrix_out.index)
        join_on = "ncbiID" #TODO maybe Troubleshooting
    else:
        axes_with_ncbiID = list(matrix.matrix_out.columns)
        join_on = "geneID"
    for ncbiID in axes_with_ncbiID:
        # get lineage of organism
        func_call = ncbi_data_handler.ncbi_lineage(ncbiID, list_lineage_order)
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

    # checks if all ranks are present in data, if not kicks them out and prints them
    rank_not_found = []
    for rank in list_lineage_order:
        if rank not in ncbiID_matrix.index:
            rank_not_found.append(rank)
    line = ""
    for el in rank_not_found:
        line = line + ", " + el
        list_lineage_order.remove(el)
    if len(line) > 0:
        line = line[2:]
        warnings.warn(f"The following ranks were not found in the NCBI IDs: {line} \n"
                      "Either they are not represented in this dataset by the given NCBI IDs, or you may have misspelled the rank.")

    # figures out the gene families
    gene_matrix = gene_annotation(data_read)

    # Tracks time if wanted
    if track_time is True:
        end = time.time()
        print(f"lineage: {end - start}s")
        end_all = time.time()
        print(f"Total runtime: {end_all-start_all}s")

    # generate UMAP
    umap_generator.generate_umap(matrix.matrix_out, ncbiID_matrix, gene_matrix, join_on, csvfile, port, colorscale, opacity,
                                 n_neighbors, min_dist, spread, seed, list_lineage_order)





# TODO Test data weg
# data = "/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile"

# main function
if __name__=="__main__":
    main()
