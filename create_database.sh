#!/bin/bash

source .env
psql -h $DATABASE_HOST -U $DATABASE_USERNAME -d $POSTGRES -p $DATABASE_PORT -a -f setup.sql
