import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale
from dash import Dash, dcc, html, Output, Input
import copy


def create_diagramm(data_matrix):
    """
    Visualizaiton of graph via plotly and dash
    :param data_matrix: contains name of organism, information of taxonomic rank, x pos and y pos
    :return:
    """
    # assigns color by dividing a colorspace from plotly into even pieces via np.linespace
    set_taxanomy = set()
    for el in data_matrix.loc[:, "lineage_label"]:  # counts every indiviual occurance of a rank
        set_taxanomy.add(el)
    n = len(set_taxanomy)
    x = np.linspace(0, 1, n)
    color_list = sample_colorscale('Rainbow', list(x)) # info over colorspaces: https://plotly.com/python/builtin-colorscales/
    color_list_hex = []
    for el in color_list: # turn RGB value into HEX value
        el = el[4:-1]
        el = el.split(sep=",")
        el = tuple((el[0].strip(), el[1].strip(), el[2].strip()))
        el = tuple((int(el[0]), int(el[1]), int(el[2])))
        el = "#{:02X}{:02X}{:02X}".format(el[0], el[1], el[2])
        color_list_hex.append(el)
    # creates dict which maps colors to a taxonomic rank
    color_dict = {}
    name_list = []
    i = 0
    for el in data_matrix.loc[:, "lineage_label"]:
        name_list.append(el)
        if el not in color_dict:
            color_dict.update({el:color_list_hex[i]})
            i = i + 1
    # creates copy of color map which
    current_color_dict = copy.deepcopy(color_dict)

    app = Dash()

    # graph object approach, ignore
    fig = go.Figure()
    for point in data_matrix.loc[:,"lineage_label"].unique():
        uniques_matrix = data_matrix[data_matrix['lineage_label'] == point]
        fig.add_trace(go.Scatter(x=uniques_matrix.loc[:, "x"], y=uniques_matrix.loc[:, "y"],
                                 customdata=[uniques_matrix.loc[:, "species_name"]],
                                 mode='markers',
                                 name=point,
                                 marker = dict(color=current_color_dict[point], size = 8),
                                 hovertemplate=f'Name: %{fig.data[0].customdata[0]}'  # klappt nicht: info soll bei hovern erscheinen
        ))

    # plotly express approach
    """fig = px.scatter(Visual_data, x=Visual_data[:,0], y=Visual_data[:,1],
                     color=label_info.loc[:,"lineage_label"], opacity=0.6) # TODO labels rausfinden"""

    app.layout = html.Div(children=[
        html.H1(children='UMAP'),
        dcc.Graph(id="graph", figure=fig, style={'width': '100vw', 'height': '90vh'})
    ])

    # Attempt to change click event, ignore
    """@app.callback(Output('graph', 'figure'),
                [Input('graph', 'restyleData')],
                prevent_initial_call = True
                )
    def update(x):
        if x == None:
            return fig
        else:
            name_item = fig.data[x[1][0]].name  # Name of legend item clicked
            print(name_item)
            if current_color_dict[name_item] == "grey": # if clicked item is of color grey, turn it back to original color
                current_color_dict.update({name_item:color_dict[name_item]})
                fig.update_traces(marker=dict(color=current_color_dict[name_item], size=8), selector=name_item)
                return fig
            else: # if clicked item is not grey, make it grey
                current_color_dict.update({name_item: "grey"})
                fig.update_traces(marker=dict(color=current_color_dict[name_item], size=8), selector = ({'name':name_item}))
                return fig"""



    # app.run_server(debug=True, use_reloader=False)
    app.run(debug=True)