from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from termcolor import cprint
from asgiref.sync import async_to_sync
from .PM_Model.PredictME_Model import run_model
import time
from termcolor import cprint
import traceback
from predict_me.my_logger import log_exception


class RunModelConsumer(WebsocketConsumer):

    def connect(self):
        try:
            self.user = self.scope.get("user")
            # self.groupname = 'data_handler_model'
            # async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
            # self.accept()
            # await self.connect()
            # cprint(self.scope, 'green')
            # cprint(self.scope.keys(), 'green')
            # cprint(dir(self.scope['user']), 'yellow')
            # await self.channel_layer.group_send(self.groupname, self.channel_name)
            self.accept()
        except Exception as ex:
            cprint(str(ex), "red")

    def disconnect(self, close_code):
        try:
            self.disconnect(close_code)
            self.close()
            cprint("Close the connection", 'green')
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            cprint(str(ex), 'red')
            log_exception(ex)

    def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data == "RUN_THE_MODEL":
                from data_handler.models import (DataFile, DataHandlerSession)
                member_data_file = DataFile.objects.get(member=self.user)
                data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file)
                donation_cols = data_session.donation_columns
                # run_model(data_session.data_file_path, donation_cols)
                run_model_data = run_model(data_session.base_data_file_path, donation_cols, self)
                if run_model_data:
                    cprint("Run model completed!", 'green')
                    data_session.pdf_report_file_path = run_model_data.get('PDF_FILE')
                    data_session.csv_report_file_path = run_model_data.get('CSV_FILE')
                    data_session.is_process_complete = True
                    data_session.save()
                    member_data_file.is_run_the_model = True
                    member_data_file.save()
                    cprint("save is run the model", 'yellow')
                    cprint('save to db done', 'yellow')
                # self.send(text_data="Run complete", close=True)
                self.send("Complete Successfully!")
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            cprint(str(ex), 'red')
            log_exception(ex)


def send_data(obj):
    try:
        obj.send(text_data=f"member_data_file")
        time.sleep(3)
        obj.send(text_data='Now sleep after sleep 3')
        time.sleep(2)
        obj.send(text_data=f"data_session")
        time.sleep(2)
        obj.send(text_data='Request complete', close=True)
    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        cprint(str(ex), 'red')
        log_exception(ex)
