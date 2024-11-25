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

# Start Timer
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

# generates Matrix by going through entire dataset and filling in a value if gene is in organism, otherwise NaN
grouped_ncbi = data_read.groupby("ncbiID")
matrix_out = pd.DataFrame()
# goes through every ncbiID and creates new df as matrix
count_droped = 0
for nID in ncbiIDs:
    x = grouped_ncbi.get_group(nID)
    new_df = x[["geneID", "FAS_F"]].copy()
    #identifying duplicates in data, keeps the largest FAS Score, discards rest
    while True: #TODO die doppelten rausholen
        duplicates = new_df.duplicated(subset="geneID",keep=False)
        if True not in duplicates.values:
            break
        subset = new_df.loc[duplicates]
        # creates subset that only contains the double element, one at every loop
        compare_element = subset.iat[0,0]
        subset_duplicates = subset[subset['geneID'] == compare_element]
        # figures out the max element and it's index
        max_score = subset_duplicates['FAS_F'].max()
        max_score_id = subset_duplicates['FAS_F'].idxmax()
        # creates list with index of the double value and removes the largest one of it
        IDs_list = subset_duplicates.index
        IDs_list = list(IDs_list.values)
        IDs_list.remove(max_score_id)
        # removes doubles from list
        new_df.drop(IDs_list, inplace=True)
        count_droped = count_droped + len(IDs_list)
    # (outer)joins dataFrames together to Matrix
    new_df.set_index('geneID', inplace=True)
    new_df.rename(columns={"FAS_F":nID}, inplace='True')
    matrix_out = matrix_out.join(new_df, how='outer')
print(f"{count_droped} were droped because of double values")
# TODO Debug also wegg
print(len(ncbiIDs), len(geneIDs))
print(len(matrix_out.axes[1]), len(matrix_out.axes[0]))
# puts mask over data, changes NaN to 0
mask_value = 0.5
matrix_out = matrix_out.map(lambda x: 1 if x >= mask_value else 0, na_action='ignore')
matrix_out.fillna(0, inplace=True)

# UMAP
reducer = umap.UMAP()
columns = matrix_out.columns
columns = list(columns.values)
features = matrix_out.loc[:,:columns[-1]]
# scaled_penguin_data = StandardScaler().fit_transform(features)
projec = reducer.fit_transform(features)

# Visualize using Plotly
fig = px.scatter(projec, x=projec[:,0], y=projec[:,1], color=matrix_out.index, labels=None) # TODO labels rausfinden

# End timer
end = time.time()
print(f"Time: {round(end-start)}s")

#fig.write_html( 'output_file_name.html', auto_open=True )
fig.show()
app = Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])
app.run_server(debug=True, use_reloader=False)
