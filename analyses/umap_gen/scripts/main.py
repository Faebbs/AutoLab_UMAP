import time

import pandas as pd
from parso.python.tree import String

import Matrix_handler
import umap_generator
import ncbi_data_handler
from analyses.umap_gen.scripts.ncbi_data_handler import ncbi_lineage


def main(file = "", separator = "\t", updateLocalDatabase=True, categorizeRank=""):
    start_all = time.time()
    # updates local ncbi Database
    if updateLocalDatabase is True:
        ncbi_data_handler.update_local_ncbi()
    # file path input
    if file == "": #TODO Fehlerbehandlung
        print("Please input file path:")
        file = input()
    try:
        data_read = pd.read_csv(file, sep=separator) #TODO Fehlerbehandlung
    except (FileNotFoundError):
        print("File could not be found")
        return

    # create Matrix of genes and if they appear in the organisms
    matrix = Matrix_handler.Matrix_ncbiID(data_read)
    matrix.create_matrix("ncbiID", "geneID", timed=True) #TODO Fehlerbehandlung


    # generates matrix with lineage of all ncbiIDs
    bad_IDs = []
    missng_IDs = []
    ncbiID_matrix = pd.DataFrame()
    start = time.time()
    for ncbiID in matrix.matrix_out.axes[0].tolist():
        # get lineage of organism
        func_call = ncbi_lineage(ncbiID)
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
    end = time.time()
    print(f"lineage: {end - start}s")
    # generate UMAP
    end_all = time.time()
    print(f"Total runtime: {end_all-start_all}s")

    # TODO weg, hier werden zwischen ergebnisse gespeichert
    #ncbiID_matrix.to_csv('/home/fabian/Documents/umap_project/analyses/umap_gen/results/lineageData.txt')
    #matrix.matrix_out.to_csv('/home/fabian/Documents/umap_project/analyses/umap_gen/results/OccuranceData.txt')

    umap_generator.generate_umap(matrix.matrix_out, ncbiID_matrix, categorizeRank=categorizeRank)



# Test data
data = "/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile"
# data = "/Users/fabia/OneDrive/Dokumente/Uni/Spez 1/Project/analyses/umap_gen/data/eukaryots.phyloprofile"

# data = "/share/gluster/Projects/vinh/fdog_ms/pp_cbm_chitin_cellulase/cell_wall.phyloprofile"
# data = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/c19a904462482430170bfe2c718775ddb7dbb885/inst/extdata/penguins.csv"

# main function
if __name__=="__main__":
    main(data, updateLocalDatabase = False, categorizeRank = "Class")
    print("")
