import pandas as pd
from pathlib import Path
from django.conf import settings
import os


def extract_columns_names(file_name):
    all_columns = []  # hold all columns in the file
    media_path = settings.MEDIA_ROOT
    df = None
    full_file_path = Path(file_name)
    # print(full_file_path)
    # print(full_file_path.exists())
    if full_file_path.exists():  # first check if the data file exists
        # check spreadsheet file extension
        if full_file_path.suffix == ".csv":
            df = pd.read_csv(os.path.join(media_path, file_name))
            all_columns = df.columns
        elif full_file_path.suffix == ".xlsx":
            df = pd.read_excel(full_file_path.as_posix())
            # iterating the columns
            # for col in df.columns:
            #     print(col)
            all_columns = df.columns

    # print(all_columns)
    return sorted(all_columns)
    # return df


def handle_uploaded_file(f, fname):
    full_path = os.path.join("media", fname)
    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)