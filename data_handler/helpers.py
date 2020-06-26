import pandas as pd
from pathlib import Path
from django.conf import settings
import os
from pprint import pprint
from .validators import *
from itertools import islice
import copy
import re
import numpy as np


validate_obj = DataValidator()

def save_data_file_rounded(file_path):
    data_file = Path(file_path)
    df = get_df_from_data_file(file_path)
    for col in df.columns.tolist():
        if df[col].dtype == "float64":
            df[col] = df[col].round()
    delete_data_file(file_path)
    if data_file.suffix == ".xlsx":
        df.to_excel(data_file.as_posix(), header=True, index=False)
    elif data_file.suffix == ".csv":
        df.to_csv(data_file.as_posix())

    print("save done")


def extract_columns_names(file_name):
    # all_columns = []  # hold all columns in the file
    all_columns = {}  # hold all columns in the file
    media_path = settings.MEDIA_ROOT
    df = None
    full_file_path = Path(file_name)
    if full_file_path.exists():  # first check if the data file exists
        # check spreadsheet file extension
        if full_file_path.suffix == ".csv":
            df = pd.read_csv(os.path.join(media_path, file_name))

        elif full_file_path.suffix == ".xlsx":
            df = pd.read_excel(full_file_path.as_posix())

        # iterating the columns
        for col in df.columns:
            # print(col)
            # print(type(df.dtypes[col]))
            all_columns[col] = str(df.dtypes[col])

    # all_columns = sorted(all_columns)
    # print(all_columns)
    return all_columns


def extract_all_column_names(file_name):
    all_columns = []  # hold all columns in the file

    media_path = settings.MEDIA_ROOT
    df = None
    full_file_path = Path(file_name)
    if full_file_path.exists():  # first check if the data file exists
        # check spreadsheet file extension
        if full_file_path.suffix == ".csv":
            df = pd.read_csv(os.path.join(media_path, file_name))

        elif full_file_path.suffix == ".xlsx":
            df = pd.read_excel(full_file_path.as_posix())

        # iterating the columns
        for col in df.columns:
            # print(col)
            # print(type(df.dtypes[col]))
            all_columns.append(col)
    # all_columns = df.columns

    # all_columns = sorted(all_columns)
    # print(all_columns)
    return all_columns


def get_row_count(file_path):
    full_file_path = Path(file_path)
    row_counts = None
    df = None
    if full_file_path.exists():  # first check if the data file exists
        # check spreadsheet file extension
        if full_file_path.suffix == ".csv":
            df = pd.read_csv(full_file_path.as_posix())

        elif full_file_path.suffix == ".xlsx":
            df = pd.read_excel(full_file_path.as_posix())
    row_counts = df.shape[0]

    return row_counts


def get_rows_data_by_columns(file_path, columns, records_count):
    columns = sorted(columns)
    all_rows = []
    data_file = Path(file_path)
    df = None
    records_count = int(records_count)
    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix(), columns=columns, convert_float=True)
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix(), columns=columns)

            # print(df[columns])
        df.fillna(method='pad')
        for c in columns:
            # this to check if the data type is float so round the values
            if df[c].dtype == "float64":
                # df[c] = df[c].apply(np.ceil)
                df[c] = df[c].round()
        rows_count = df.shape[0]
        current_record_data = {}
        previous_50_count = records_count - 50
        for index, row in islice(df.iterrows(), previous_50_count, records_count):
            # index is the index in the data frame
            # row is the series object
            # breakpoint()
            for col in columns:
                # print(index, "----> ", col, "--->", row[col], end='\n')
                tmp_cell_val = row[col]
                current_record_data["ID"] = index
                current_record_data[col] = validate_obj.detect_and_validate(replace_nan_value(tmp_cell_val))
                # print(col, current_record_data[col])
                # breakpoint()
            all_rows.insert(0, current_record_data)
            current_record_data = {}

    print(all_rows[0])
    return all_rows


def get_rows_data_by_search_query(file_path, columns, search_query):
    columns = sorted(columns)
    all_rows = []
    data_file = Path(file_path)
    search_query = str(search_query)
    df = None
    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix(), columns=columns)
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix(), columns=columns)

            # print(df[columns])
        df.fillna(method='pad')
        rows_count = df.shape[0]
        # mask = df[columns].applymap(lambda x: search_query in str(x))
        # mask = df[columns].apply(lambda x: any(x.astype(str).str.contains(search_query)))
        # mask = df[[columns].str.contains("Boston")]
        # df2 = df.loc[mask, columns]

        current_record_data = {}
        for index, row in df.iterrows():
            # index is the index in the data frame
            # row is the series object
            # breakpoint()
            for col in columns:
                # print(index, "----> ", col, "--->", row[col], end='\n')
                if row.str.contains(search_query).any() is True:
                    tmp_cell_val = row[col]
                    current_record_data["ID"] = index
                    current_record_data[col] = validate_obj.detect_and_validate(replace_nan_value(tmp_cell_val))

            if current_record_data:  # check if the dictionary is empty or contain elements
                all_rows.insert(0, current_record_data)
            current_record_data = {}

    # print(all_rows[0])
    return all_rows


def get_not_validate_rows(file_path, all_columns, column_name):
    all_columns = sorted(all_columns)
    all_rows = []
    data_file = Path(file_path)
    df = None

    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix(), columns=column_name)
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix(), columns=column_name, skipinitialspacebool=True)

        # df.fillna(method='pad')
        row_count = df.shape[0]
        current_record = []  # will be dynamic record, will indicate to current row in the loop, then set it to null
        # column_mask = (df[column_name] == "NaN")
        column_mask = df[column_name].isnull()
        # df2 = df.loc[column_mask]  # data frame of elements which null
        df2 = df.loc[column_mask, all_columns]  # data frame of elements which null
        # print(type(df2))
        # print(df2)

        current_record_data = {}
        for index, row in df2.iterrows():
            # row is the series object
            for col in all_columns:
                # print(index, "----> ", col, "--->", row[col], end='\n')
                tmp_cell_val = row[col]
                current_record_data["ID"] = index
                current_record_data[col] = validate_obj.detect_and_validate(replace_nan_value(tmp_cell_val))
            all_rows.insert(0, current_record_data)
            current_record_data = {}

        # breakpoint()
    # print(all_rows)
    print(len(all_rows))
    return all_rows


SELECTED_COLUMN = ""  # global to call when access the series
ERROR_ROWS_IDXS = []  # the rows which contains error or not validate data


def get_not_validate_rows2(file_path, column_name, all_columns, records_count=50):
    global SELECTED_COLUMN, ERROR_ROWS_IDXS
    SELECTED_COLUMN = column_name
    # print(SELECTED_COLUMN)
    all_columns = sorted(all_columns)
    errors_idx_lst = []
    all_rows = []
    data_file = Path(file_path)
    df = None
    records_count = int(records_count)
    print(records_count)
    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix())
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix(), skipinitialspacebool=True)

        # df.fillna(method='pad')

    for tupls in df.itertuples():
        row_as_dict = tupls._asdict()
        for key, value in row_as_dict.items():
            if key == column_name:
                curr_row = validate_obj.detect_and_validate(str(value))
                if curr_row['is_error'] is True:
                    errors_idx_lst.append(row_as_dict['Index'])

    df_error = df.copy().reindex(errors_idx_lst)
    df_correct = df.loc[~df.index.isin(errors_idx_lst)]
    print("Correct Rows", len(df_correct))
    print("Not Correct Rows", len(df_error))
    # df_error = df_error.append(df_correct, ignore_index=True)
    df_error = df_error.append(df_correct)
    print("All Rows", len(df_error))
    # print(df_error.head())

    current_record_data = {}

    previous_50_count = records_count - 50

    for index, row in islice(df_error.iterrows(), previous_50_count, records_count):
    # for index, row in results.iterrows():
        # row is the series object
        for col in all_columns:
            # print(index, "----> ", col, "--->", row[col], end='\n')
            tmp_cell_val = row[col]
            current_record_data["ID"] = index
            current_record_data[col] = validate_obj.detect_and_validate(replace_nan_value(tmp_cell_val))
        # all_rows.insert(0, current_record_data)
        all_rows.append(current_record_data)

        current_record_data = {}

    # del results, df_copy_error_data, df_copy_correct_data, frames
    # print(len(all_rows))
    return all_rows


def validate_series(data_value: pd.Series):
    global ERROR_ROWS_IDXS
    # print(type(data_value), data_value)
    # print(type(data_value.name))
    if data_value.name == SELECTED_COLUMN:
        for index, row in data_value.iteritems():
            # print(type(index), type(row))
            # print(f"Index : {index}, Row : {row}")
            curr_row = validate_obj.detect_and_validate(str(row))
            if curr_row["is_error"] is True:
                ERROR_ROWS_IDXS.append(int(index))
                # print(curr_row)




def update_rows_data(file_path, data_json, column_names):
    all_rows = []
    data_file = Path(file_path)
    rows_and_values = {}
    df = None
    for key, value in data_json.items():
        rows_and_values[key.split('_')[1]] = value
    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix(), columns=column_names)
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix(), columns=column_names, skipinitialspacebool=True)

    # df2 = copy.deepcopy(df[column_names])
    df2 = copy.deepcopy(df)
    for key, value in rows_and_values.items():
        # {"0": [{"colName", "colValue"}, {"colName", "colValue"}]
        for val in value:
            df2.at[int(key), val['colName']] = val['colValue']

    # save all changes to the file

    if data_file.suffix == ".xlsx":
        df2.to_excel(data_file.as_posix(), header=True, index=False)
    elif data_file.suffix == ".csv":
        df2.to_csv(data_file.as_posix())


def validate_data_type_in_dualbox(columns: dict, data_file_path, columns_list):
    """
        This function when the member press validate the data type in the dual
        box before click on process and navigate to the data handler page
        ["", "object", "int64", "float64", 'bool', 'datetime64', 'category', 'timedelta'];
    """
    result_dict = {}  # the return dict with validate values
    df = get_df_from_data_file(data_file_path)
    # print(dict(df.dtypes))

    for col_name, data_type in columns.items():
        # check what is the data type depends on that call the right method from validate obj
        if data_type == "int64":
            # tmp = df[col_name].apply(validate_obj.is_valid_number)
            # print(df[col_name][tmp])
            df[col_name].astype(str).str.isdigit()




def get_df_from_data_file(file_path):
    data_file = Path(file_path)
    df = None
    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix())
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix(), skipinitialspacebool=True)

    return df
def replace_nan_value(value):
    """
    function will return the same value from column or series of data file
    in string to avoid the error when convert string to json object in datatable js file

    Arguments:
        value {value} -- the nan value from pandas series or column

    Returns:
        value -- return the same value even if it is nan but in string
    """
    return str(value)


def delete_data_file(path):
    """ Deletes file from filesystem. """
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")


def validate_column_date_type(columns):
    data_file = Path(file_path)
    df = None

    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix())
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix())


def handle_uploaded_file(f, fname):
    full_path = os.path.join("media", fname)
    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
