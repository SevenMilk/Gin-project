from datetime import datetime,timedelta
import requests, pendulum, time, ast
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

class Ruten_DA():
    def __init__(self,con_id):
        self.SLACK_CONN_ID = con_id
        self.local_tz = pendulum.timezone("Asia/Taipei")

    def convert_datetime(self,datetime_string):
        return datetime_string.astimezone(self.local_tz).strftime('%b-%d %H:%M:%S')

    def project_alert(self,context):
        '''Adapted from https://medium.com/datareply/integrating-slack-alerts-in-airflow-c9dcd155105
             Sends message to a slack channel.
                If you want to send it to a "user" -> use "@user",
                    if "public channel" -> use "#channel",
                    if "private channel" -> use "channel"
        '''
        slack_webhook_token = BaseHook.get_connection(self.SLACK_CONN_ID).password
        # slack_webhook_token = "T03UFH34T5Y/B03U8UTT02J/s2cZlPiRo0HfqvZYax2zzh5J"
        #channel = BaseHook.get_connection(self.SLACK_CONN_ID).login
        slack_msg = f"""
            :red_circle: Task Failed.
            *Task*: {context.get('dag_run').get_task_instances(state='failed')[0].task_id}
            *Dag*: {context.get('dag_run').get_task_instances(state='failed')[0].dag_id}
            *Execution Time*: {self.convert_datetime(context.get('next_execution_date'))}
            *Params*: {context.get('params')}
            *Monitor*: {context.get('dag').owner}
            <{context.get('dag_run').get_task_instances(state='failed')[0].log_url.replace("192.168.23.130:8085//",Variable.get('airflow_host'))}|*Logs*>
        """

        slack_alert = SlackWebhookOperator(
            task_id='slack_alert',
            webhook_token=slack_webhook_token,
            message=slack_msg,
            http_conn_id=self.SLACK_CONN_ID
        )

        return slack_alert.execute(context=context)

