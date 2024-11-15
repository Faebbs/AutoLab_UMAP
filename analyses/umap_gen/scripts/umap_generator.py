import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import seaborn as sns
import umap.umap_ as umap
import plotly.express as px
import matplotlib.pyplot as plt
from dash import Dash, dcc, html
import time

start = time.time()

# Test data
# data_read = pd.read_csv("/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile", sep="\t")
# data_read = pd.read_csv("/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile", sep="\t", nrows=20000)
data_read = pd.read_csv("/Users/fabia/OneDrive/Dokumente/Uni/Spez 1/Project/analyses/umap_gen/data/eukaryots.phyloprofile", sep="\t")

# data_read = pd.read_csv("/share/gluster/Projects/vinh/fdog_ms/pp_cbm_chitin_cellulase/cell_wall.phyloprofile", sep="\t")
# data_read = pd.read_csv("https://raw.githubusercontent.com/allisonhorst/palmerpenguins/c19a904462482430170bfe2c718775ddb7dbb885/inst/extdata/penguins.csv")


# drops NAs
print(len(data_read))
data_read.dropna(how='any', inplace=True)
print(len(data_read))

# group by ncbiID
grouped_ncbi = data_read.groupby(data_read.ncbiID)
IDs = set(data_read["ncbiID"].tolist()) # set of every ncbiID
# creates first dataframe
for ID in IDs:
    data_read_grouped = grouped_ncbi.get_group(ID)
    IDs.remove(ID)
    break
# iterate though all ncbiIDs and creates a dataframe for every one
for ID in IDs:
    data_read_group = grouped_ncbi.get_group(ID)
    data_read_grouped = pd.merge(data_read_grouped, data_read_group, how="outer", on="ncbiID")
    print(data_read_grouped.head())
print(data_read_grouped.head())


# UMAP
reducer = umap.UMAP()
features = data_read[['FAS_F']].values
# scaled_penguin_data = StandardScaler().fit_transform(features)
projec = reducer.fit_transform(features)

# Visualize using Plotly
fig = px.scatter(projec, x=projec[:,0], y=projec[:,1], color=data_read.ncbiID, labels={'color':'ncbiID'})

end = time.time()
print(f"Time: {round(end-start)}s")

fig.write_html( 'output_file_name.html', auto_open=True )
'''app = Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])
app.run_server(debug=True, use_reloader=False)'''
