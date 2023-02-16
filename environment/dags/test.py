from datetime import datetime
from datetime import timedelta
import pendulum
import time
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
import pytz
from template.slack import Ruten_DA


local_tz = pendulum.timezone("Asia/Taipei")
args = {
        'owner': 'ericjiang',
        'start_date': datetime(2021, 6, 24, tzinfo=local_tz),
        'depends_on_past': False,
        'retries': 0,
        'retry_delay': timedelta(minutes=1),
        'queue' : 'data-analyze'
}

alert_callback = Ruten_DA("slack_Ruten_DA")
with DAG('test_slack', description='test_slack',schedule_interval=None,dagrun_timeout=timedelta(minutes=600),
                        tags=['slack'],on_failure_callback=alert_callback.project_alert ,default_args = args,catchup=False) as dag:

    test = BashOperator(
           task_id='sleep',
           bash_command="eceho hello hadoop216"
    )
    Done = DummyOperator(task_id='Done')
    test >> Done