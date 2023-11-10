#!/bin/bash

source .env
psql -h $DBHOST -U $DBUSER -d $DBNAME -p $DBPORT -a -f setup.sql
