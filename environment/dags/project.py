#! /usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import pendulum
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.dummy import DummyOperator
from template.slack import Ruten_DA

local_tz = pendulum.timezone("Asia/Taipei")
args = {
        'owner': 'ericjiang',
        'start_date': datetime(2023, 2, 15, tzinfo=local_tz),
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'queue': 'data-analyze'
}

alert_callback = Ruten_DA("slack_Ruten_DA")
with DAG('smart_city_taipei', description='專案',schedule_interval="00 10 * * *",dagrun_timeout=timedelta(hours=1),
                              on_failure_callback=alert_callback.project_alert,max_active_runs=1,
                              tags=['TAIPEI'],default_args = args,catchup=False,params={"dt":""}) as dag:
    job = DockerOperator(
                task_id='smart_city_taipei',
                image='moonlight165/gin_project:0.0.1',
                cpus=0.5,
                mem_limit='512m',
                api_version='auto',
                auto_remove = True,
                command='/bin/bash -c /home/ericjiang/python/run.sh ',
                docker_url='unix://var/run/docker.sock',
                network_mode='bridge'
    )

    Start = DummyOperator(task_id='Start')
    Done = DummyOperator(task_id='Done', dag=dag, trigger_rule='all_success')

    Start >> job >> Done