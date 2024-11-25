import numpy as np
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import umap
import plotly.express as px
from dash import Dash, dcc, html

def generate_umap(matrix):
    # UMAP
    reducer = umap.UMAP()
    columns = matrix.columns
    columns = list(columns.values)
    features = matrix.loc[:,:columns[-1]]
    # scaled_penguin_data = StandardScaler().fit_transform(features)
    projec = reducer.fit_transform(features)

    # Visualize using Plotly
    fig = px.scatter(projec, x=projec[:,0], y=projec[:,1], color=matrix.index, labels=None) # TODO labels rausfinden

    #fig.write_html( 'output_file_name.html', auto_open=True )
    fig.show()
    app = Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(debug=True, use_reloader=False)
