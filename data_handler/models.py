from django.db import models
# from membership.models import UserMembership
# Create your models here.
from django.contrib.auth import get_user_model
import pandas as pd
import json
import traceback
from termcolor import cprint
from predict_me.my_logger import log_exception

UPLOAD_PROCEDURES = (
    ("local_file", "Local File"),
    ("google_plus", "Google Plus",),
    ("one_drive", "One Drive"),
    ("dropbox", "Dropbox"),
    ("none", "None")
)

DATA_HANDLER_SESSION_NAMES = (
    ("upload", "Upload"),
    ("pick_columns", "Pick Columns"),
    ("data_process", "Data Processing"),
    ("run_modal", "Run Predictive Modal")
)


class DataFile(models.Model):
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True,
                               related_name='member_data_file')
    allowed_records_count = models.IntegerField(null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    has_sessions = models.BooleanField(default=False)
    last_uploaded_session = models.IntegerField(null=True, blank=True)

    class Meta:
        # verbose_name = "member_data_file"
        db_table = 'member_data_files'

    def __str__(self):
        return f"Data file object for {self.member}, Allowed Records count {self.allowed_records_count}"

    @property
    def get_fields_as_list(self):
        fields = self._meta.fields
        fields_list = []
        for fid in fields:
            fields_list.append(fid.name)
        return fields_list


class DataHandlerSession(models.Model):
    data_handler_id = models.ForeignKey(to=DataFile, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='data_sessions_set')
    file_upload_procedure = models.CharField(max_length=20, null=True, blank=True, choices=UPLOAD_PROCEDURES)
    data_file_path = models.CharField(max_length=255, blank=True, null=True)
    current_session_name = models.CharField(max_length=70, null=True, blank=True, choices=DATA_HANDLER_SESSION_NAMES)
    run_modal_date_time = models.CharField(null=True, blank=True, max_length=60)
    data_handler_session_label = models.CharField(max_length=70, null=True, blank=True)
    selected_columns = models.TextField(null=True, blank=True)
    selected_columns_dtypes = models.TextField(null=True, blank=True)
    donor_id_column = models.CharField(max_length=150, null=False, blank=True)
    is_donor_id_selected = models.BooleanField(null=True, blank=True, default=False)
    unique_id_column = models.CharField(max_length=200, null=True, blank=True)
    all_columns_with_dtypes = models.TextField(null=True, blank=True)
    is_process_complete = models.BooleanField(null=True, blank=True, default=False)
    all_records_count = models.BigIntegerField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        # verbose_name = "member_data_file"
        db_table = 'data_handler_sessions'

    def __str__(self):
        return f"{self.data_handler_session_label}"

    @property
    def get_fields_as_list(self):
        fields = self._meta.fields
        fields_list = []
        for fid in fields:
            fields_list.append(fid.name)
        return fields_list

    @property
    def get_selected_columns_as_list(self):
        # return self.selected_columns.split("|")
        # return sorted(self.selected_columns.split("|"))
        try:
            return self.selected_columns.split("|")
        except AttributeError as aex:
            pass
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())

    @property
    def get_selected_columns_with_dtypes(self):
        columns_with_dtypes = {}

        try:
            all_text = self.selected_columns_dtypes.split("|")
            for txt in all_text:
                col_name, col_dtype = txt.split(":")
                columns_with_dtypes[col_name] = col_dtype

        except ValueError:
            pass
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
        finally:
            return columns_with_dtypes

    @property
    def get_all_columns_with_dtypes(self):
        columns_with_dtypes = {}

        try:
            all_cols = self.selected_columns_dtypes.split("|")
            for col in all_cols:
                col_name, col_dtype = col.split(":")
                columns_with_dtypes[col_name] = col_dtype

        except ValueError:
            pass
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
        finally:
            return columns_with_dtypes

    @property
    def get_selected_columns_casting(self):
        columns_casting_dtypes = {}
        try:
            all_cols = self.selected_columns_dtypes.split("|")

            for col in all_cols:
                col_name, col_dtype = col.split(":")
                col_name = col_name.strip()
                # check what the kind of selected column, to place the convenient data type for casting
                if col_dtype.startswith('numeric') or col_dtype.startswith('donation'):
                    # columns_casting_dtypes[col_name] = lambda x: round(int(x)) if isinstance(x, int) else str(x) or round(int(x)) if isinstance(x, float) else str(x)
                    columns_casting_dtypes[col_name] = pd.to_numeric()
                elif col_dtype.startswith('text'):
                    columns_casting_dtypes[col_name] = str

        except ValueError:
            pass
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
        finally:
            return columns_casting_dtypes

    @property
    def get_all_data_file_columns(self):
        cols_all_dtype = {}
        try:
            all_cols_str = self.all_columns_with_dtypes.split("|")
            for col in all_cols_str:
                if col != "":
                    col_nm, col_tp = col.split(":")
                    cols_all_dtype[col_nm] = col_tp

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
        except Exception as ex:
            log_exception(traceback.format_exc())
        finally:
            return cols_all_dtype


class MemberDownloadCounter(models.Model):
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True,
                               related_name='download_counter')
    is_accept_terms = models.BooleanField(null=True, blank=True, default=False)
    is_accept_download_template = models.BooleanField(null=True, blank=True,
                                                      default=False)  # this when the member check he download
    is_download_template = models.BooleanField(null=True, blank=True,
                                               default=False)  # this if the member download the template or not
    download_counter = models.IntegerField(null=True, blank=True, default=0)
    date_inserted = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'members_download_counter'
