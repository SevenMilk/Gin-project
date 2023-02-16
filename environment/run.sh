#!/bin/bash

docker compose -f serving.yml up -d
docker compose -f airflow_online.yml up -d
