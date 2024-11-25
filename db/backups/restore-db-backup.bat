@echo off

REM Restore a backup of the postgres database in the ./backups/melanoma_segmentation_db-backup.sql.gz file.
REM Delete the database if it already exists.

set DB_NAME=melanoma_segmentation_db

REM Change directory to the script's location
cd /d "%~dp0"

REM Terminate active connections to the database
psql -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '%DB_NAME%' AND pid <> pg_backend_pid();"

REM Drop the database if it exists
psql -U postgres -c "DROP DATABASE IF EXISTS \"%DB_NAME%\";"

REM Create the database again
psql -U postgres -c "CREATE DATABASE \"%DB_NAME%\";"

REM Restore the database using 7-Zip to extract the backup
"C:\Program Files\7-Zip\7z.exe" e ./backups/%DB_NAME%-backup.sql.gz -o./backups -y

REM Import the SQL backup into PostgreSQL
psql -U postgres -d %DB_NAME% -f ./backups/%DB_NAME%-backup.sql

REM Clean up extracted SQL file
del ./backups/%DB_NAME%-backup.sql

@echo Done