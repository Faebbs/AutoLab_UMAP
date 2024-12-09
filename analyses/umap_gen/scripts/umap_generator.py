import numpy as np
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import umap
import plotly.express as px
from dash import Dash, dcc, html

def generate_umap(matrix_values, matrix_lineage, categorizeRank=""):
    # UMAP
    reducer = umap.UMAP()
    # scaled_penguin_data = StandardScaler().fit_transform(features)
    transformed_data = reducer.fit_transform(matrix_values)

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


    # Visualize using Plotly
    fig = px.scatter(transformed_data, x=transformed_data[:,0], y=transformed_data[:,1], color=matrix_values.index, labels=None) # TODO labels rausfinden

    #fig.write_html( 'output_file_name.html', auto_open=True )
    fig.show()
    app = Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(debug=True, use_reloader=False)
