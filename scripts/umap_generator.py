import pandas as pd
import umap
import os
from scripts import plotly_handler
from pathlib import Path


def generate_umap(matrix_values, matrix_lineage, gene_matrix, join_on, to_csv, port, colorscale, opacity, n_neighbors, min_dist, spread, seed, list_lineage_order):
    """
    Runs UMAP Algorithm to reduce dimensions of occurrence data
    :param matrix_values: Occurrence data
    :param matrix_lineage: Matrix with ncbiID and all rank names
    :param gene_matrix: Gene Matrix
    :param join_on: Column used as new lines
    :param to_csv: Enables write to csv
    :param port: Port
    :param colorscale: Colorscale used for
    :param opacity: Opacity value of the points in the plot
    :param n_neighbors: The size of local neighborhood (in terms of number of neighboring sample points) used for manifold approximation.
                        Larger values result in more global views of the manifold, while smaller values result in more local data being preserved.
                        In general values should be in the range 2 to 100.
    :param min_dist: The effective minimum distance between embedded points. Smaller values will result in a more clustered/clumped
                     embedding where nearby points on the manifold are drawn closer together, while larger values will result on a more
                     even dispersal of points. The value should be set relative to the spread value, which determines the scale at which embedded points will be spread out.
    :param spread: The effective scale of embedded points. In combination with min_dist this determines how clustered/clumped the embedded points are.
    :param seed: If int, random_state is the seed used by the random number generator; If RandomState instance,
                 random_state is the random number generator; If None, the random number generator is the RandomState instance used by np.random.
    :param list_lineage_order: List of lineage ranks that will be analysed
    :return:
    """
    # UMAP
    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        spread=spread,
        random_state=seed
    )
    # scaled_penguin_data = StandardScaler().fit_transform(features)
    transformed_data = reducer.fit_transform(matrix_values)

    # creates matrix with all necessary information
    indexes = list(matrix_values.index.values) # List with indices corresponding to the rows of transformed_data
    matrix_of_wisdom = pd.DataFrame(indexes)

    # creates Matrix with ncbiIDs
    if join_on == "ncbiID":
        # rename first column
        matrix_of_wisdom.rename(columns={0: "ncbiID"})
        # assigns the organisms their corresponding rank names
        for categorizeRank in list_lineage_order:
            info_of_label = []
            for el in matrix_of_wisdom.loc[:,0]:
                info_of_label.append(matrix_lineage.loc[categorizeRank][el])
            info_of_label = pd.DataFrame(info_of_label)
            matrix_of_wisdom[categorizeRank] = info_of_label

        # Adds positional matrix to label matrix
        matrix_of_wisdom["x"] = transformed_data[:, 0]
        matrix_of_wisdom["y"] = transformed_data[:, 1]

        # adds the name of species
        info_of_label = []
        for el in matrix_of_wisdom.loc[:, 0]:
            info_of_label.append(matrix_lineage.loc["species"][el])
        info_of_label = pd.DataFrame(info_of_label)
        matrix_of_wisdom["species_name"] = info_of_label
    elif join_on == "geneID":
        # rename first column
        matrix_of_wisdom.rename(columns={0:"geneID"}, inplace=True)

        # Adds positional matrix to label matrix
        matrix_of_wisdom["x"] = transformed_data[:, 0]
        matrix_of_wisdom["y"] = transformed_data[:, 1]
        # adds the gene families
        matrix_of_wisdom = matrix_of_wisdom.merge(gene_matrix, on="geneID", how="outer")

    # writes data used for plot generation to matrix
    if to_csv is True:
        path_from_root = Path(__file__).parent.parent
        path_resluts = os.path.join(path_from_root, "results/matrixdata.txt")
        matrix_of_wisdom.to_csv(path_resluts, sep="\t", index=False)

    # creates Diagram with plotly depending on ncbi or gene
    if join_on == "ncbiID":
        plotly_handler.create_diagramm_ncbi(matrix_of_wisdom, port, colorscale, opacity, list_lineage_order)
    else:
        plotly_handler.create_diagramm_gene(matrix_of_wisdom, port, colorscale, opacity)


# Debugging purposes
if __name__ == "__main__":
    generate_umap(pd.DataFrame(), pd.DataFrame(), to_csv=False, port=8050, colorscale="Rainbow")