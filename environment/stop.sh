#!/bin/bash

docker compose -f serving.yml down
docker compose -f airflow_online.yml down
