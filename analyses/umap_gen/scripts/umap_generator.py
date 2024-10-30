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
data_read = pd.read_csv("/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile", sep="\t", nrows=20000)
# data_read = pd.read_csv("/share/gluster/Projects/vinh/fdog_ms/pp_cbm_chitin_cellulase/cell_wall.phyloprofile", sep="\t")
print(len(data_read))
data_read.dropna(how='any', inplace=True)
print(len(data_read))

# gene classes
list_cl = set()
for line in data_read.index:
    ID = data_read["geneID"][line]
    spliced = ID.split("_")
    list_cl.add(spliced[0])
print(list_cl)

# UMAP
reducer = umap.UMAP()
features = data_read[['FAS_F']].values
projec = reducer.fit_transform(features)
#projec = reducer.fit_transform(features)

# Visualize using Plotly
fig = px.scatter(projec, x=projec[:,0], y=projec[:,1], color=data_read.ncbiID, labels={'color':'ncbiID'})
fig.show()

end = time.time()
print(f"Time: {round(end-start)}s")

app = Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])

app.run_server(debug=True, use_reloader=False)
