#!/bin/bash

# Restore a backup of the postgres database in the ./backups/melanoma_segmentation_db-backup.sql.gz file.
# Delete the database if it already exists.

cd "$(dirname "$0")"

DB_NAME="melanoma_segmentation_db"

psql -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();"
psql -U postgres -c "DROP DATABASE IF EXISTS \"$DB_NAME\";"
psql -U postgres -c "CREATE DATABASE \"$DB_NAME\";"
gunzip -c ./backups/${DB_NAME}-backup.sql.gz | psql -U postgres -d $DB_NAME
