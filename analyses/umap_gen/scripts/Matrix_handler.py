from typing import List, Any

import pandas as pd
import time

class Matrix_ncbiID:
    def __init__(self, data):
        self.data = data
        self.matrix_out = None

    def create_matrix(self, row_value, column_value, mask_value=0.5, timed=False):
        if timed is True:
            # Start Timer
            start = time.time()

        # drops NAs for faster matrix creation
        self.data.dropna(how='any', inplace=True)


        # group by ncbiID
        columnIDs = list(set(self.data[column_value].tolist())) # unsorted list of every ncbiID (once)
        rowIDs = list(set(self.data[row_value].tolist())) # unsorted list of every geneID (once)

        # generates Matrix by going through entire dataset and filling in a value if gene is in organism, otherwise NaN
        grouped_ncbi = self.data.groupby(column_value)
        matrix_out = pd.DataFrame()
        # goes through every column_value and creates new df as matrix
        count_droped = 0
        for nID in columnIDs:
            x = grouped_ncbi.get_group(nID)
            new_df = x[[row_value, "FAS_F"]].copy()
            #identifying duplicates in data, keeps the largest FAS Score, discards rest
            while True:
                duplicates = new_df.duplicated(subset=row_value,keep=False)
                if True not in duplicates.values:
                    break
                subset = new_df.loc[duplicates]
                # creates subset that only contains the double element, one at every loop
                compare_element = subset.iat[0,0]
                subset_duplicates = subset[subset[row_value] == compare_element]
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
            new_df.set_index(row_value, inplace=True)
            new_df.rename(columns={"FAS_F":nID}, inplace='True')
            matrix_out = matrix_out.join(new_df, how='outer')
        print(f"{count_droped} were droped because of double values") #TODO drinlasssen?
        # puts mask over data, changes NaN to 0
        matrix_out = matrix_out.map(lambda x: 1 if x >= mask_value else 0, na_action='ignore')
        matrix_out.fillna(0, inplace=True)

        if timed is True:# End timer
            end = time.time()
            print(f"Runtime of matrix creation: {end-start}s")
            self.matrix_out = matrix_out