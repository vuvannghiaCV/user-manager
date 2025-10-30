#!/bin/bash

bash /wait-for-it.sh ${POSTGRES_HOST}:${POSTGRES_PORT-5432} -- echo ">>> ${POSTGRES_HOST}:${POSTGRES_PORT-5432} <<<"

cd /app
alembic upgrade head
python main.py
