import numpy as np
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import umap
import plotly.express as px
from dash import Dash, dcc, html

def generate_umap(matrix_values, matrix_lineage, rank = ""):
    # UMAP
    reducer = umap.UMAP()
    columns = matrix_values.columns
    columns = list(columns.values)
    features = matrix_values.loc[:, :columns[-1]]
    # scaled_penguin_data = StandardScaler().fit_transform(features)
    projec = reducer.fit_transform(features)

    # TODO weg, hier werden zwischen ergebnisse gespeichert
    """file = open('/home/fabian/Documents/umap_project/analyses/umap_gen/results/UmapData.txt', "w")
    file.write("x,y\n")
    for i in projec:
        line = ""
        line = line + str(i[0]) + "," + str(i[1]) + "\n"
        file.write(line)
    file.close()"""

    # Visualize using Plotly
    fig = px.scatter(projec, x=projec[:,0], y=projec[:,1], color=matrix_values.index, labels=None) # TODO labels rausfinden

    #fig.write_html( 'output_file_name.html', auto_open=True )
    fig.show()
    app = Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(debug=True, use_reloader=False)
