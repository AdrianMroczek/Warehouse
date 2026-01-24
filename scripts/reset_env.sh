#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

LOG=${1:-"restock_log.txt"}
DATABASE=${2:-"stocks.db"}

DB_PATH="$SCRIPT_DIR/../db/$DATABASE"
LOG_PATH="$SCRIPT_DIR/$LOG"

if [ -f "$LOG" ]; then
  echo "Deleting LOG_FILE"
  rm -f "$LOG"
else
    echo "Log file $LOG not found, skipping."
fi

if [ -f "$DB_PATH" ]; then
  echo "Deleting DB"
  rm -f "$DB_PATH"
else
    echo "Database $DB_PATH not found, skipping."
fi

echo "------------------------------"
echo "Environment reset complete."