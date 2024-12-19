import numpy as np
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale
from dash import Dash, dcc, html, Output, Input, callback
import webbrowser
from threading import Timer
import threading
import dash_bootstrap_components as dbc

def open_browser(port):
	webbrowser.open_new("http://localhost:{}".format(port))

def run_dash(app, port):
    Timer(1, open_browser(port)).start();
    app.run_server(port=port, use_reloader=False)

def create_diagramm(data_matrix, port, colorscale, opacity):
    """
    Creates a plotly plot in a Dash app.
    :param data_matrix: Matrix with information for plotly graph object
    :param port: Port, default=8050
    :param colorscale: Choose one of Plotlys colorscales, default="Rainbow"; more colorscale options: https://plotly.com/python/builtin-colorscales/
    :return:
    """

    app = Dash(external_stylesheets=[dbc.themes.SUPERHERO])

    # creates dict of lineage for slider
    list_lineage_order = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
    marks_dict = {}
    i = 0
    while i < len(list_lineage_order):
        marks_dict.update({i:list_lineage_order[i]})
        i = i + 1

    # Layout for slider
    body = dbc.Container([
            dbc.Row([
                html.Div(
                    dcc.Slider(0, len(list_lineage_order)-1, step=1,
                               marks=marks_dict, value=0, id="rank_slider"), style={'width': '80vw'})
            ], justify="center", align='center')
        ])
    # puts together layout for entire app
    app.layout = html.Div(children=[
        dcc.Graph(id="graph", style={'width': '100vw', 'height': '90vh'}),
        body
    ])

    # callback for slider: lets you decide which rank should be displayed in the legend and by color coding
    @callback(
        Output("graph", "figure"),
        Input("rank_slider", "value")
    )
    def update_figure(selected_rank, colorscale=colorscale):
        """
        Callback for slider.
        :param selected_rank:
        :param colorscale:
        :return:
        """
        selected_rank = marks_dict[selected_rank]
        # assigns color by dividing a colorspace from plotly into even pieces via np.linespace
        set_taxanomy = list()
        for el in data_matrix.loc[:, selected_rank].unique():  # counts every indiviual occurance of a rank
            set_taxanomy.append(el)
        n = len(set_taxanomy)
        x = np.linspace(0, 1, n)
        color_list = sample_colorscale(colorscale=colorscale, samplepoints=list(x))  # info over colorspaces: https://plotly.com/python/builtin-colorscales/
        color_list_rgba = []
        for el in color_list:  # turn RGB value into RGBA Value (with opacity)
            el = el[0:3] + "a" + el[3:-1] + ", " + opacity + ")"
            color_list_rgba.append(el)
        # creates dict which maps colors to a taxonomic rank
        color_dict = {}
        name_list = []
        i = 0
        for el in set_taxanomy:
            if el not in color_dict:
                color_dict.update({el: color_list_rgba[i]})
                i = i + 1

        # graph object approach
        fig = go.Figure()
        for point in data_matrix.loc[:, selected_rank].unique():
            uniques_matrix = data_matrix[data_matrix[selected_rank] == point]
            customdf = np.stack((uniques_matrix.loc[:, "species_name"], uniques_matrix.loc[:, 0], uniques_matrix.loc[:, selected_rank]), axis=-1) # necessary for use in customdata
            fig.add_trace(go.Scatter(x=uniques_matrix.loc[:, "x"], y=uniques_matrix.loc[:, "y"],
                                     customdata=customdf,
                                     mode='markers',
                                     name=point,
                                     marker=dict(color=color_dict[point], size=9, line=dict(width=0.2, color='black')),
                                     hovertemplate="<b>%{customdata[0]}</b><br>" +
                                                   "%{customdata[2]}<br>" +
                                                   "NCBI Id: %{customdata[1]}<br><br>" +
                                                   "x: %{x}<br>" +
                                                   "y: %{y}" +
                                                   "<extra></extra>",
                                     ))
        fig.update_layout()
        return fig

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

    # Run Dash in a separate thread
    dash_thread = threading.Thread(target=run_dash(app, port))
    dash_thread.start()

