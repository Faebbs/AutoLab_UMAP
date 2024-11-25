import pandas as pd
import Matrix_handler
import umap_generator


def main(file = "", separator = "\t"):
    if file == "": #TODO Fehlerbehandlung
        print("Please input file path:")
        file = input()
    try:
        data_read = pd.read_csv(file, sep=separator) #TODO Fehlerbehandlung
    except (FileNotFoundError):
        print("File could not be found")
        return

    matrix = Matrix_handler.Matrix_ncbiID(data_read)
    matrix2 = Matrix_handler.Matrix_ncbiID(data_read)

    matrix.create_matrix("ncbiID", "geneID", timed=True) #TODO Fehlerbehandlung
    matrix2.create_matrix("geneID", "ncbiID", timed=True)

    umap_generator.generate_umap(matrix.matrix_out)




# Test data
data = "/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile"
# data = "/Users/fabia/OneDrive/Dokumente/Uni/Spez 1/Project/analyses/umap_gen/data/eukaryots.phyloprofile"

# data = "/share/gluster/Projects/vinh/fdog_ms/pp_cbm_chitin_cellulase/cell_wall.phyloprofile"
# data = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/c19a904462482430170bfe2c718775ddb7dbb885/inst/extdata/penguins.csv"

# main function
if __name__=="__main__":
    main(data)
    print("")
