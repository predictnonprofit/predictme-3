import pandas as pd
from pathlib import Path
from django.conf import settings
import os
from prettyprinter import pprint
from .validators import *
from itertools import islice
from termcolor import cprint
import traceback
from predict_me.my_logger import (log_exception, log_info)

validate_obj = DataValidator()


def clean_currency(x: str):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    try:
        # x = str(x)
        if isinstance(x, str):
            if x.startswith("$"):
                return x.replace('$', '').replace(',', '')
        # return float(x)
        return x
    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def get_selected_columns_as_list(member_data_file):
    """
    this function will take DataFile object, to return selected columns as list
    Args:
        member_data_file:

    Returns:
        list
    """
    return member_data_file.get_selected_columns_as_list


def save_data_file_rounded(file_path):
    data_file = Path(file_path)
    df = get_df_from_data_file(file_path)
    df_copy = df.copy()
    saved_logged_msg = ''  # the info log will save, contains columns name, columns dtypes
    saved_logged_cols_base = []  # the columns with dtype log will save, contains columns name, columns dtypes
    saved_logged_cols_after = []  # the columns with converted dtype
    new_cleand_cols = []  # this list all hold all columns without any spaces or whitespaces
    # Volunteered in the past
    # cprint(df.dtypes, 'green')
    try:

        for col in df_copy.columns.tolist():
            new_cleand_cols.append(col.strip())
            saved_logged_cols_base.append(f"{col}: {df_copy[col].dtype}")
            if df_copy[col].dtype == "float64":
                df_copy[col] = df_copy[col].round().astype('int64')
            elif df_copy[col].dtype == "object":
                df_copy[col] = df_copy[col].str.strip()
                df_copy[col] = df_copy[col].apply(clean_currency)
            if df_copy[col].dtype == "bool":
                df_copy[col] = df_copy[col].astype(str)
            saved_logged_cols_after.append(f"{col}: {df_copy[col].dtype}")

        # the messages will save the logs of data file columns
        msg_str_before = '\n'.join(saved_logged_cols_base)
        msg_str_after = '\n'.join(saved_logged_cols_after)
        saved_logged_msg = "\nMain Column with Data type: \n[\n {} \n]\n Converted Columns data type: \n[\n {} \n]\n".format(
            msg_str_before, msg_str_after)
        log_info(saved_logged_msg)
        delete_data_file(file_path)
        if data_file.suffix == ".xlsx":
            df_copy.to_excel(data_file.as_posix(), header=new_cleand_cols, index=False)
        elif data_file.suffix == ".csv":
            df_copy.to_csv(data_file.as_posix(), header=new_cleand_cols, index=False, sep=',')

        cprint("save done", 'green')
    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        delete_data_file(file_path)
        log_exception(traceback.format_exc())


def download_data_file_converter(member_data_file):
    selected_columns = member_data_file.get_selected_columns_as_list
    data_file_path = Path(member_data_file.data_file_path)
    df = get_df_from_data_file(data_file_path)
    try:
        if data_file_path.suffix == ".xlsx":

            df.to_excel(data_file_path.as_posix(), header=True, index=False, columns=selected_columns)
        elif data_file_path.suffix == ".csv":
            df.to_csv(data_file_path.as_posix(), header=True, index=False, columns=selected_columns)
    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def extract_all_columns_with_dtypes(file_name):
    try:
        all_columns = {}  # hold all columns in the file

        df = get_df_from_data_file(file_name)

        # iterating the columns
        for col in df.columns:
            # print(col)
            # print(type(df.dtypes[col]))
            all_columns[col] = str(df.dtypes[col])

        # all_columns = sorted(all_columns)
        # print(all_columns)
        return all_columns

    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def extract_all_column_names(file_name):
    try:
        all_columns = []  # hold all columns in the file

        df = get_df_from_data_file(file_name)
        full_file_path = Path(file_name)

        # iterating the columns
        for col in df.columns:
            # print(col)
            # print(type(df.dtypes[col]))
            all_columns.append(col)
        # all_columns = df.columns

        # all_columns = sorted(all_columns)
        # print(all_columns)
        return all_columns
    except Exception as ex:
        cprint(str(ex), 'red')
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def get_row_count(file_path):
    full_file_path = Path(file_path)
    row_counts = None
    df = get_df_from_data_file(file_path)
    row_counts = df.shape[0]
    return row_counts


def get_rows_data_by_columns(file_path, columns, records_count, columns_with_types, all_original_columns):
    try:
        all_rows = []
        # print(columns)
        df = get_df_from_data_file(file_path)
        records_count = int(records_count)
        previous_50_count = int(records_count - 50)
        print(previous_50_count, records_count)
        # df2 = df.loc[previous_50_count:records_count, columns]
        # print(df2)
        current_record_data = {}
        for index, row in islice(df[columns].iterrows(), previous_50_count, records_count):
            # print(index)
            # index is the index in the data frame
            # row is the series object
            idx = index
            for col in columns:
                # print(row[col])
                # print(idx, col)
                tmp_cell_val = row[col]
                current_record_data["ID"] = idx
                tmp_cell_val = replace_nan_value(tmp_cell_val)
                # tmp_cell_val = tmp_cell_val.rstrip('0').rstrip('.') if '.' in tmp_cell_val else tmp_cell_val
                # print(columns_with_types[col], tmp_cell_val)
                current_record_data[col] = validate_obj.detect_and_validate(tmp_cell_val,
                                                                            dtype=columns_with_types[col], original_dtype=all_original_columns[col])
                # print(idx, "--> ", current_record_data[col])
            all_rows.insert(0, current_record_data)
            current_record_data = {}

        # print(len(all_rows))
        # pprint(all_rows)
        # check if the length of all_rows < 0 means no records to show
        if len(all_rows) <= 0:
            return 0
        else:
            return all_rows
    except Exception as ex:
        # cprint(str(ex), 'red')
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def get_rows_data_by_search_query(file_path, columns, search_query, columns_with_dtypes):
    try:
        all_rows = []
        search_query = str(search_query)
        df = get_df_from_data_file(file_path)

        current_record_data = {}
        for index, row in df.iterrows():
            # index is the index in the data frame
            # row is the series object

            for col in columns:
                # print(index, "----> ", col, "--->", row[col], end='\n')

                if row.str.contains(search_query, case=False).any() is True:
                    # print(row.str.contains(search_query, case=False).any())
                    tmp_dtype = columns_with_dtypes[col]
                    tmp_cell_val = row[col]
                    current_record_data["ID"] = index
                    tmp_cell_val = replace_nan_value(tmp_cell_val)
                    current_record_data[col] = validate_obj.detect_and_validate(tmp_cell_val, dtype=tmp_dtype)

            if current_record_data:  # check if the dictionary is empty or contain elements
                all_rows.insert(0, current_record_data)
            current_record_data = {}

        # print(all_rows[0])
        if len(all_rows) <= 0:
            return 0
        else:
            return all_rows
    except Exception as ex:
        cprint(str(ex), 'red')
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def get_not_validate_rows(file_path, all_columns, column_name):
    # all_columns = sorted(all_columns)
    all_rows = []
    data_file = Path(file_path)
    df = get_df_from_data_file(file_path)

    # df.fillna(method='pad')
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


def get_not_validate_rows2(file_path, column_name, all_columns, columns_with_dtypes, records_count=50):
    try:
        global SELECTED_COLUMN, ERROR_ROWS_IDXS
        SELECTED_COLUMN = column_name
        # print(SELECTED_COLUMN)
        # all_columns = sorted(all_columns)
        errors_idx_lst = []
        all_rows = []
        df = get_df_from_data_file(file_path)
        records_count = int(records_count)
        # print(records_count)

        for index, row in df.iterrows():
            # print(index, row)
            # print(row.name)
            for col in all_columns:
                if col == column_name:
                    tmp_dtype = columns_with_dtypes[col]
                    curr_row = validate_obj.detect_and_validate(row[col], dtype=tmp_dtype)
                    if curr_row['is_error'] is True:
                        errors_idx_lst.append(index)

        df_error = df.copy().reindex(errors_idx_lst)
        df_correct = df.loc[~df.index.isin(errors_idx_lst)]
        cprint(f"Valid Rows {len(df_correct)}", 'green')
        cprint(f"Not Valid Rows {len(df_error)}", "red")
        # df_error = df_error.append(df_correct, ignore_index=True)
        # df2 = pd.concat([df_error, df_correct], ignore_index=False)
        # pprint(df_correct)
        # df_error = df_error.append(df_correct)
        df_concat_errors = pd.concat([df_error, df_correct])
        cprint(f"All Rows {len(df_error)}", 'yellow')
        # print(df_error)
        current_record_data = {}
        rows_count = df.shape[0]
        x_total = int(int(rows_count / 50) * 50)
        cprint(x_total, 'blue')
        # rows_list = (x for x in range(0, rows_count))
        rows_array = np.arange(0, rows_count)
        rows_array2 = ""
        # rows_array = np.delete(rows_array, 5)
        # cprint(len(rows_array), "green")
        # pprint(df_error.tail())
        previous_50_count = records_count - 50
        print(previous_50_count, records_count)
        for index, row in islice(df_error.iterrows(), previous_50_count, records_count):
            # for index, row in results.iterrows():
            # row is the series object
            for col in all_columns:
                # print(index, "----> ", col, "--->", row[col], end='\n')
                tmp_dtype = columns_with_dtypes[col]
                tmp_cell_val = row[col]
                tmp_cell_val = replace_nan_value(tmp_cell_val)
                current_record_data["ID"] = index
                current_record_data[col] = validate_obj.detect_and_validate(tmp_cell_val, dtype=tmp_dtype)
            # all_rows.insert(0, current_record_data)
            all_rows.append(current_record_data)
            current_record_data = {}
        tmm = df_correct.index.tolist()
        valide_df = df.loc[tmm, all_columns]
        all_rows2 = []
        # check if it is the last page
        if x_total == records_count or x_total == 0:
            for idx, row in valide_df.iterrows():
                for col in valide_df.columns:
                    tmp_dtype = columns_with_dtypes[col]
                    tmp_cell_val = row[col]
                    tmp_cell_val = replace_nan_value(tmp_cell_val)
                    current_record_data["ID"] = idx
                    current_record_data[col] = validate_obj.detect_and_validate(tmp_cell_val, dtype=tmp_dtype)
                all_rows2.append(current_record_data)
                current_record_data = {}

        all_rows = all_rows + all_rows2
        all_rows.reverse()  # to reverse list make valid rows in the last
        # del results, df_copy_error_data, df_copy_correct_data, frames
        print(len(all_rows))
        # print(all_rows2[::-1])
        # pprint(all_rows2)
        if len(all_rows) <= 0:
            return 0
        else:
            if x_total <= 50:
                return all_rows[::-1]
            else:
                return all_rows

    except Exception as ex:
        cprint(str(ex), 'red')
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


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


def update_rows_data(file_path, data_json, column_names, columns_with_dtypes):
    # pd.describe_option("display.float_format")
    # pd.set_option("display.float_format", "{:.2f}".format)
    try:
        data_file = Path(file_path)
        all_rows = []
        rows_and_values = {}
        df = get_df_from_data_file(file_path)
        for key, value in data_json.items():
            # ROW_0 [{'colName': 'Cand_Name', 'colValue': '858f'}]

            rows_and_values[key.split('_')[1]] = value

        # df2 = copy.deepcopy(df[column_names])
        # df2 = copy.deepcopy(df)
        df2 = df.copy()
        current_value = ""
        for key, value in rows_and_values.items():
            # {"0": [{"colName", "colValue"}, {"colName", "colValue"}]
            # 0 [{'colName': 'Cand_Name', 'colValue': '858fx'}]
            # print(key, value)
            for val in value:
                cprint(df2[val['colName']].dtype, 'yellow')
                current_value = val['colValue']
                if df2[val['colName']].dtype == 'int64':
                    if current_value.isdigit():
                        df2.at[int(key), val['colName']] = current_value
                    else:
                        df2[val['colName']] = df2[val['colName']].astype(str)
                        df2.at[int(key), val['colName']] = current_value
                        # df2[val['colName']] = df2[val['colName']].astype(int)
                        # df2[val['colName']] = pd.to_numeric(df2[val['colName']], errors='ignore', downcast='float')
                        # df2[val['colName']] = pd.to_numeric(df2[val['colName']])
                        # df2[val['colName']] = df2[val['colName']].astype('int64')
                else:
                    df2.at[int(key), val['colName']] = current_value

                cprint(df2[val['colName']].dtype, 'blue')

        # save all changes to the file
        if data_file.suffix == ".xlsx":
            df2.to_excel(data_file.as_posix(), header=True, index=False)
        elif data_file.suffix == ".csv":
            df2.to_csv(data_file.as_posix(), header=True, index=False)
        cprint(df2.dtypes, 'magenta')
        # return "Data saved successfully"
        return current_value, "Data saved successfully"

    except Exception as ex:
        cprint(str(ex), 'red')
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


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
    # return value


def delete_data_file(path):
    """ Deletes file from filesystem. """
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def reorder_columns(the_reset_of_column, is_dict=False):
    """
    this function will reorder the selected columns to make the unique column is the first one
    Args:
        the_reset_of_column:

    Returns: the_reset_of_column

    """

    unique_idx = "unique identifier (id)"
    unique_col = ''

    try:
        if is_dict is False:
            for col in the_reset_of_column:
                if unique_idx in col.lower():
                    idx = the_reset_of_column.index(col)
                    unique_col = col
                    del the_reset_of_column[idx]
                    the_reset_of_column.insert(0, unique_col)

            return the_reset_of_column
        else:
            new_ordered_list = []
            for col_name, col_dtype in the_reset_of_column.items():
                if unique_idx in col_dtype:
                    new_ordered_list.insert(0, col_name)
                else:
                    new_ordered_list.append(col_name)

            return new_ordered_list

    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def validate_column_date_type(columns):
    data_file = Path(file_path)
    df = None

    if data_file.exists():
        if data_file.suffix == ".xlsx":
            df = pd.read_excel(data_file.as_posix())
        elif data_file.suffix == ".csv":
            df = pd.read_csv(data_file.as_posix(), skipinitialspace=True)


def handle_uploaded_file(f, fname):
    full_path = os.path.join("media", fname)
    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def check_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def delete_all_member_data_file_info(member_data_file):
    """
    this function will take DataFile object, to reset all member data file
    Args:
        member_data_file:

    Returns:

    """
    try:
        from data_handler.models import DataHandlerSession
        for dfile in DataHandlerSession.objects.filter(data_handler_id=member_data_file):
            delete_data_file(dfile.data_file_path)
        DataHandlerSession.objects.filter(data_handler_id=member_data_file).delete()
        # member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file)
        # member_data_file.data_file_path = "None"
        # member_data_file.file_upload_procedure = "None"
        # member_data_file.all_records_count = 0
        # member_data_file.selected_columns = ""
        # member_data_file.selected_columns_dtypes = ""
        # member_data_file.donor_id_column = ""
        # member_data_file.is_donor_id_selected = False
        # member_data_file.unique_id_column = ""
        # member_data_file.all_columns_with_dtypes = ""
        # member_data_file.is_process_complete = False
        # member_data_file.save()
    except DataHandlerSession.DoesNotExist:
        cprint('DataHandlerSession.DoesNotExist', 'red')

    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def convert_dfile_with_selected_columns(df: pd.DataFrame, selected_columns: list, file_path: Path, file_ext: str):
    try:
        parent_dir = Path() / file_path.parent
        df_selected_columns = df[selected_columns]
        if file_ext == "xlsx":
            full_file_path = Path() / f"{os.path.splitext(file_path.name)[0]}.xlsx"
            df_selected_columns.to_excel(full_file_path, header=True, index=False)
            return full_file_path
        elif file_ext == "csv":
            full_file_path = Path() / f"{os.path.splitext(file_path.name)[0]}.csv"
            df_selected_columns.to_csv(full_file_path, header=True, index=False)
            return full_file_path
    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def get_df_from_data_file(file_path):
    try:
        from data_handler.models import DataHandlerSession
        data_file = Path(file_path)
        file_object = DataHandlerSession.objects.filter(data_file_path=data_file.as_posix()).first()
        df = None
        # cprint(file_object.get_all_data_file_columns, 'yellow')
        if file_object:
            if data_file.exists():
                if data_file.suffix == ".xlsx":
                    df = pd.read_excel(data_file.as_posix())
                elif data_file.suffix == ".csv":
                    df = pd.read_csv(data_file.as_posix(), sep=',',
                                     skipinitialspace=True)
        else:
            if data_file.exists():
                if data_file.suffix == ".xlsx":
                    df = pd.read_excel(data_file.as_posix())
                elif data_file.suffix == ".csv":
                    df = pd.read_csv(data_file.as_posix(), sep=',')

        # cprint(df.dtypes, 'red')
        # this for fill the empty cells with its own empty values
        float_cols = df.select_dtypes(include=['float64']).columns
        str_cols = df.select_dtypes(include=['object']).columns
        int_cols = df.select_dtypes(include=['int64']).columns
        df.loc[:, float_cols] = df.loc[:, float_cols].fillna(0)
        df.loc[:, int_cols] = df.loc[:, int_cols].fillna(0)
        df.loc[:, str_cols] = df.loc[:, str_cols].fillna('NULL')
        df_clone = df.copy()

        # this loop to convert bool dtype to string
        for co in df_clone.columns.tolist():
            if df_clone[co].dtype == 'bool':
                # cprint(df_clone[co].dtype, 'blue')
                df_clone[co] = df_clone[co].apply(str)
                # cprint(df_clone[co].dtype, 'green')
            elif df_clone[co].dtype == 'float64':
                df_clone[co] = df_clone[co].round().astype(int)

        cprint(df_clone.dtypes, 'green')


        return df_clone

    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def check_empty_df(file_path):
    try:
        df = get_df_from_data_file(file_path)
        if df.empty is True:
            return True
        return False
    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


def check_data_or_num(params: str):
    try:
        data_or_num = ''
        last_param = params.strip().split('/')[-1]
        if last_param == '':
            last_param = params.strip().split('/')[-2]
        if last_param.isdigit():
            data_or_num = int(last_param)
        else:
            data_or_num = 'data'
        return data_or_num
    except AttributeError:
        pass
    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())
