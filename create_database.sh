#!/bin/bash

source .env
psql -h $DATABASE_HOST -U $DATABASE_USERNAME -d $POSTGRES -p $DATABASE_PORT -v dbname=$DATABASE_NAME -a -f setup.sql

python3 pipeline/etl/setup.py