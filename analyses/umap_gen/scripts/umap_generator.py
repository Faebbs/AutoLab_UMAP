import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import seaborn as sns
import umap
import plotly.express as px
import matplotlib.pyplot as plt
from dash import Dash, dcc, html
import time

start = time.time()

# Test data
data_read = pd.read_csv("/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile", sep="\t")
# data_read = pd.read_csv("/home/felixl/PycharmProjects/cellulases/data/filtered/eukaryots.phyloprofile", sep="\t", nrows=20000)
# data_read = pd.read_csv("/Users/fabia/OneDrive/Dokumente/Uni/Spez 1/Project/analyses/umap_gen/data/eukaryots.phyloprofile", sep="\t")

# data_read = pd.read_csv("/share/gluster/Projects/vinh/fdog_ms/pp_cbm_chitin_cellulase/cell_wall.phyloprofile", sep="\t")
# data_read = pd.read_csv("https://raw.githubusercontent.com/allisonhorst/palmerpenguins/c19a904462482430170bfe2c718775ddb7dbb885/inst/extdata/penguins.csv")


# drops NAs
print(len(data_read))
data_read.dropna(how='any', inplace=True)
print(len(data_read))

# group by ncbiID
ncbiIDs = list(set(data_read["ncbiID"].tolist())) # unsorted list of every ncbiID (once)
geneIDs = list(set(data_read["geneID"].tolist())) # unsorted list of every geneID (once)

# goes through entire dataset and fills in a value if gene is in organism, otherwise NaN
grouped_ncbi = data_read.groupby("ncbiID")
matrix_out = pd.DataFrame()

# goes through every ncbiID and creates new df as matrix
for nID in ncbiIDs:
    x = grouped_ncbi.get_group(nID)
    new_df = x[["geneID", "FAS_F"]].copy()
    #identifying duplicates in data
    to_remove = []
    while True: #TODO die doppelten rausholen
        duplicates = new_df.duplicated(keep=False)
        if True not in duplicates.values:
            break
        subset = new_df.loc[duplicates]
        # subset.reset_index(inplace=True)
        # subset.set_index('geneID', inplace=True)
        # keeps the largest FAS Score, discards rest
        y = [subset.iat[0,0]]
        subset_duplicates = subset.isin(y) #makes a boolean mask over df
        subset_duplicates = subset.loc[subset_duplicates['FAS_F']] #TODO klappt nicht
        max_score = max(subset_duplicates.loc[:,'FAS_F'])

    new_df.drop() #TODO duplikate aus new_df rausholen





    # new_df.drop_duplicates(subset="geneID", keep='first', inplace=True, ignore_index=True) # TODO was soll mit doppelten Daten passieren?

    new_df.set_index('geneID', inplace=True)
    new_df.rename(columns={"FAS_F":nID}, inplace='True')
    # joins dfs together
    matrix_out = matrix_out.join(new_df, how='outer')

# puts mask over data, changes NaN to 0
mask_value = 0.5
matrix_out = matrix_out.map(lambda x: 1 if x >= mask_value else 0, na_action='ignore')
matrix_out.fillna(0, inplace=True)

# matrix_out.to_csv("matrix_debug.txt", index=True) #TODO debug also weg

# UMAP
reducer = umap.UMAP()
columns = matrix_out.columns
columns = list(columns.values)
features = matrix_out.loc[:,:columns[-1]]
# scaled_penguin_data = StandardScaler().fit_transform(features)
projec = reducer.fit_transform(features)

# Visualize using Plotly
fig = px.scatter(projec, x=projec[:,0], y=projec[:,1], color=matrix_out.index, labels=None) # TODO labels rausfinden

end = time.time()
print(f"Time: {round(end-start)}s")

#fig.write_html( 'output_file_name.html', auto_open=True )
fig.show()
app = Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])
app.run_server(debug=True, use_reloader=False)
