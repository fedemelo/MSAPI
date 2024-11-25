#!/bin/bash

# Create a backup of the melanoma_segmentation_db database and compress it with gzip.

cd "$(dirname "$0")"

DB_NAME="melanoma_segmentation_db"
FILE="${DB_NAME}-backup.sql"
BACKUP_DIR="./backups"

pg_dump -U postgres $DB_NAME > $BACKUP_DIR/$FILE
gzip $BACKUP_DIR/$FILE
