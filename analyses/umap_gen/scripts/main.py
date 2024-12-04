import pandas as pd
import Matrix_handler
import umap_generator
import ncbi_data_handler
from analyses.umap_gen.scripts.ncbi_data_handler import ncbi_lineage


def main(file = "", separator = "\t", updateLocalDatabase = True):
    # updates local ncbi Database
    if updateLocalDatabase is True:
        ncbi_data_handler.update_local_ncbi()

    if file == "": #TODO Fehlerbehandlung
        print("Please input file path:")
        file = input()
    try:
        data_read = pd.read_csv(file, sep=separator) #TODO Fehlerbehandlung
    except (FileNotFoundError):
        print("File could not be found")
        return

    # create Matrix
    matrix = Matrix_handler.Matrix_ncbiID(data_read)
    # matrix2 = Matrix_handler.Matrix_ncbiID(data_read)

    matrix.create_matrix("ncbiID", "geneID", timed=True) #TODO Fehlerbehandlung
    # matrix2.create_matrix("geneID", "ncbiID", timed=True)


    # generates matrix with lineage of all ncbiIDs
    #TODO Fehlerbehandlung
    ncbiID_matrix = pd.DataFrame()
    print(len(matrix.matrix_out.axes[0].tolist()))
    for ncbiID in matrix.matrix_out.axes[0].tolist():
        func_call = ncbi_lineage(ncbiID)
        if isinstance(func_call, str):
            print("Fehler")
            continue
        df_ncbi_lineage = pd.DataFrame.from_dict(func_call, orient="index")
        new_df = pd.DataFrame({"Rank": df_ncbi_lineage.axes[0].tolist() , ncbiID: df_ncbi_lineage.values.tolist()})
        new_df.set_index("Rank", inplace=True)
        ncbiID_matrix = ncbiID_matrix.join(new_df, how="outer")

    print(ncbiID_matrix)
    print(" ")

    # generate UMAP
    #umap_generator.generate_umap(matrix.matrix_out)



# Test data
data = "/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile"
# data = "/Users/fabia/OneDrive/Dokumente/Uni/Spez 1/Project/analyses/umap_gen/data/eukaryots.phyloprofile"

# data = "/share/gluster/Projects/vinh/fdog_ms/pp_cbm_chitin_cellulase/cell_wall.phyloprofile"
# data = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/c19a904462482430170bfe2c718775ddb7dbb885/inst/extdata/penguins.csv"

# main function
if __name__=="__main__":
    main(data, updateLocalDatabase = False)
    print("")
