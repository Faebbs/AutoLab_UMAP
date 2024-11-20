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
ncbiIDs = list(set(data_read["ncbiID"].tolist())) # unsorted list of every ncbiID (once)
geneIDs = list(set(data_read["geneID"].tolist())) # unsorted list of every geneID (once)

'''
# creates matrix though python list
matrix_out = [["/"]]
for i in range(len(geneIDs)): # creates columns
    matrix_out[0].append(geneIDs[i])
for i in range(len(ncbiIDs)): # creates rows
    matrix_out.append([ncbiIDs[i]])'''

# goes through entire dataset and fills in a value if gene is in organism, otherwise np.NaN
grouped_ncbi = data_read.groupby("ncbiID")
matrix_out = pd.DataFrame()

# goes through every ncbiID and creates new df with geneID as index and FAS_f as only value
for nID in ncbiIDs:
    x = grouped_ncbi.get_group(nID)
    new_df = x[["geneID", "FAS_F"]].copy()
    new_df.drop_duplicates(subset="geneID", keep='first', inplace=True, ignore_index=True) # TODO was soll mit doppelten Daten passieren?
    new_df.set_index('geneID', inplace=True)
    new_df.rename(columns={"FAS_F":nID}, inplace='True')
    # joins dfs together
    matrix_out = matrix_out.join(new_df, how='outer')

print(len(ncbiIDs), len(geneIDs))
print("--------")
print(matrix_out.info())


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
