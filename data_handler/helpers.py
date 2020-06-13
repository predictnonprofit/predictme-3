import pandas as pd
from pathlib import Path
from django.conf import settings
import os
from pprint import pprint
from .validators import *


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
    print(all_columns)
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
    print(all_columns)
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


def get_rows_data_by_columns(file_path, columns, row_count):
    columns = sorted(columns)
    all_rows = []
    data_file = Path(file_path)
    df = None

    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix(), columns=columns)
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix(), columns=columns)

            # print(df[columns])
        df.fillna(method='pad')
        row_count = df.shape[0]
        current_record = []  # will be dynamic record, will indicate to current row in the loop, then set it to null 
        current_record_data = {}
        for i in range(len(df[columns])):
            for col in columns:
                tmp_cell_val = df[columns].loc[i, col]
                current_record_data["ID"] = i
                current_record_data[col] = validate_empty(replace_nan_value(tmp_cell_val))
                # print(validate_empty(replace_nan_value(tmp_cell_val)))
                # print(i, '->', col, "-> ", df[columns].loc[i, col]) 
            all_rows.insert(0, current_record_data)
            # all_rows.append(current_record_data)
            current_record_data = {}

    # print(type(all_rows.reverse()))
    # print(all_rows[0])
    return all_rows


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
