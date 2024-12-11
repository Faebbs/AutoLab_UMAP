import numpy as np
import seaborn as sns
from ete3.utils import color
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import umap
import colorsys
import plotly.express as px

from analyses.umap_gen.scripts.plotly_handler import create_diagramm


def generate_umap(matrix_values, matrix_lineage, categorizeRank="species", debug_mode=False):
    if debug_mode is False:
        # UMAP
        reducer = umap.UMAP()
        # scaled_penguin_data = StandardScaler().fit_transform(features)
        transformed_data = reducer.fit_transform(matrix_values)
    else: # Debug Mode: read data from files
        matrix_values = pd.read_csv("/home/fabian/Documents/umap_project/analyses/umap_gen/results/OccuranceData.txt")
        matrix_values.set_index("ncbiID", inplace=True)
        matrix_lineage = pd.read_csv("/home/fabian/Documents/umap_project/analyses/umap_gen/results/lineageData.txt")
        matrix_lineage.set_index("Rank", inplace=True)
        file = open("/home/fabian/Documents/umap_project/analyses/umap_gen/results/UmapData.txt","r")
        transformed_data = []
        for line in file:
            try:
                line = line.strip()
                lineel = line.split(sep=",")
                transformed_data.append( [float(lineel[0]), float(lineel[1])] )
            except(TypeError, ValueError):
                continue
        transformed_data = np.array(transformed_data)

    # TODO weg, hier werden zwischen ergebnisse gespeichert
    """file = open('/home/fabian/Documents/umap_project/analyses/umap_gen/results/UmapData.txt', "w")
    file.write("x,y\n")
    for i in transformed_data:
        line = ""
        line = line + str(i[0]) + "," + str(i[1]) + "\n"
        file.write(line)
    file.close()"""

    # setting labels
    # TODO labels sollen gruppiert werden nach der lineage, dafür muss color/label? gesetzt werden, aber wie?
    indexes = list(matrix_values.index.values) # List with indices corresponding to the rows of transformed_data
    matrix_of_wisdom = pd.DataFrame(indexes)
    # assigns the entrys the rank by which they should be classified
    info_of_label = []
    for el in matrix_of_wisdom.loc[:,0]:
        info_of_label.append(matrix_lineage.loc[categorizeRank][el])
    info_of_label = pd.DataFrame(info_of_label)
    matrix_of_wisdom["lineage_label"] = info_of_label

    # Adds positional matrix to label matrix
    matrix_of_wisdom["x"] = transformed_data[:, 0]
    matrix_of_wisdom["y"] = transformed_data[:, 1]

    create_diagramm(matrix_of_wisdom)

# Debugging purposes
if __name__ == "__main__":
    generate_umap(pd.DataFrame(), pd.DataFrame(),categorizeRank="class", debug_mode=True)