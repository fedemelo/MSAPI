@echo off

REM Create a backup of the melanoma_segmentation_db database and compress it with 7-Zip.

set DB_NAME=melanoma_segmentation_db
set FILE=%DB_NAME%-backup.sql
set BACKUP_DIR=./backups

REM Change directory to the script's location
cd /d "%~dp0"

REM Create a backup of the PostgreSQL database
pg_dump -U postgres -d %DB_NAME% -f %BACKUP_DIR%\%FILE%

REM Compress the backup file using 7-Zip
"C:\Program Files\7-Zip\7z.exe" a %BACKUP_DIR%\%DB_NAME%-backup.sql.gz %BACKUP_DIR%\%FILE%

REM Remove the uncompressed SQL file after compression
del %BACKUP_DIR%\%FILE%

@echo Done!
