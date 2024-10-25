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

# Test data
data_read = pd.read_csv("/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile", sep="\t")
print(len(data_read))
data_read.dropna(how='any')
print(len(data_read))

# Test UMAP
reducer = umap.UMAP()
umap_data = data_read[
    [
        "FAS_F",
        "FAS_B"
    ]
].values
scaled_data = StandardScaler().fit_transform(umap_data)
embedding = reducer.fit_transform(scaled_data)


fig = px.scatter(
    x=embedding[:, 0],
    y=embedding[:, 1],
    #color=[sns.color_palette()[x] for x in penguins.species.map({"Adelie":0, "Chinstrap":1, "Gentoo":2})],
    title='UMAP projection of the eukaryots dataset'
)

fig.show()

'''app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)'''
