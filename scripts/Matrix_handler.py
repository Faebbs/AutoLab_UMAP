import pandas as pd
import time
import numpy as np

class Matrix_ncbiID:
    """
    Class for occurrence Matrix
    """
    def __init__(self, data):
        self.data = data
        self.matrix_out = None

    def combine_data(self, occurance_data, new_identifier):
        """
        Combines data if more than one occurrence data column is given
        :param occurance_data: Name of columns which are used as Value in occurrence matrix
        :param new_identifier: Big string to avoid double columns
        :return:
        """
        list_values = []
        n = 0
        for el in occurance_data:
            value_array = self.data.loc[:, el]
            value_array = value_array.to_numpy()
            value_array = np.nan_to_num(value_array)
            list_values.append(value_array)
            n = n + 1
        result = list_values[0]
        i = 1
        while i < len(list_values):
            result = np.add(result, list_values[i])
            i = i + 1
        avg_func = np.vectorize(lambda x: x / n)
        result = avg_func(result)

        result = pd.DataFrame(result)
        self.data[new_identifier] = result.loc[:, 0] # Wierd string as identifier so no double column problem should occur

    def create_matrix(self, genecolumn, ncbiidcolumn, join_on, occurance_data, mask_value, track_time):
        """
        Creates the occurrence matrix with given occurrence data
        :param genecolumn: Column in which the geneIDs are stored
        :param ncbiidcolumn: Column in which the ncbiIDs are stored
        :param join_on: Column which will be used as new rows (ncbiID or geneID)
        :param occurance_data: Column which stores the occurrence data
        :param mask_value: Occurrence data threshold
        :param track_time: Enables tracking time
        :return:
        """
        if track_time is True:
            # Start Timer
            start = time.time()

        new_identifier = "occurance_data+fdybnjio98pnzwsev3948w0anpv"
        self.combine_data(occurance_data, new_identifier)

        # drops NAs for faster matrix creation
        self.data.dropna(how='any', inplace=True)

        # assigns rows: column in data which was given through parameter joinon
        row_value = join_on
        # assigns columns: data which is not given through parameter joinon
        if join_on == genecolumn:
            column_value = ncbiidcolumn
        else:
            column_value = genecolumn

        # group by ncbiID
        columnIDs = list(set(self.data[column_value].tolist())) # unsorted list of every ncbiID (once)

        # generates Matrix by going through entire dataset and filling in a value if gene is in organism, otherwise NaN
        grouped_ncbi = self.data.groupby(column_value)
        matrix_out = pd.DataFrame()
        # goes through every column_value and creates new df as matrix
        count_droped = 0
        for nID in columnIDs:
            x = grouped_ncbi.get_group(nID)
            new_df = x[[row_value, new_identifier]].copy()
            # identifying duplicates in data, keeps the largest FAS Score, discards rest
            while True:
                duplicates = new_df.duplicated(subset=row_value,keep=False)
                if True not in duplicates.values:
                    break
                subset = new_df.loc[duplicates]
                # creates subset that only contains the double element, one at every loop
                compare_element = subset.iat[0,0]
                subset_duplicates = subset[subset[row_value] == compare_element]
                # figures out the max element and it's index
                max_score = subset_duplicates[new_identifier].max()
                max_score_id = subset_duplicates[new_identifier].idxmax()
                # creates list with index of the double value and removes the largest one of it
                IDs_list = subset_duplicates.index
                IDs_list = list(IDs_list.values)
                IDs_list.remove(max_score_id)
                # removes doubles from list
                new_df.drop(IDs_list, inplace=True)
                count_droped = count_droped + len(IDs_list)
            # (outer)joins dataFrames together to Matrix
            new_df.set_index(row_value, inplace=True)
            new_df.rename(columns={new_identifier:nID}, inplace='True')
            matrix_out = matrix_out.join(new_df, how='outer')
        # puts mask over data if value is given
        if mask_value is not None:
            matrix_out = matrix_out.map(lambda x: 1 if x >= mask_value else 0, na_action='ignore')
        # changes NaN to 0
        matrix_out.fillna(0, inplace=True)

        self.matrix_out = matrix_out

        if track_time is True:# End timer
            end = time.time()
            print(f"Runtime of matrix creation: {end-start}s")