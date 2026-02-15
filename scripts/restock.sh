#!/bin/bash

# This script automates the process of managing inventory item quantities.
# It reads item details from a CSV file and update inventory.
# CSV structure: name,price,quantity,category_name with first line as header.
# Non existent items will be created, existing items will have their quantities and prices updated.
# To lower the quantity, use a negative number.
# Usage: ./restock.sh [csv_file] [api_url]

#Log file creation and date entry
LOG_FILE="restock_log.txt"
touch "$LOG_FILE"
ENTRY_DATE=$(date +"%Y-%m-%d %T")

exec > >(tee -a "$LOG_FILE") 2>&1

echo "$ENTRY_DATE"

CSV=${1:-"dostawa.csv"}
URL=${2:-"http://127.0.0.1:8000/api/employee/products"}

echo $URL
echo $CSV

grep -v '^$' "$CSV" | tail -n +2 | while IFS=',' read -r NAME PRICE QUANTITY CATEGORY || [ -n "$NAME" ]
do
  NAME=$(echo "$NAME" | tr -d '\r'| sed '1s/^\xEF\xBB\xBF//')
  PRICE=$(echo "$PRICE" | tr -d '\r')
  QUANTITY=$(echo "$QUANTITY" | tr -d '\r')
  CATEGORY=$(echo "$CATEGORY" | tr -d '\r')

  if [ "$NAME" == "Name" ] || [ -z "$NAME" ]; then
    continue
  fi


  echo "Restocking item: $NAME, Price: $PRICE, Quantity: $QUANTITY, Category: $CATEGORY"

  # Create temporary JSON payload file
  cat <<EOF > payload.json
{
  "name": "$NAME",
  "price": $PRICE,
  "quantity": $QUANTITY,
  "category_name": "$CATEGORY"
}
EOF

  curl -s -X 'POST' "$URL" \
     -H 'Content-Type: application/json; charset=utf-8' \
     --data-binary @payload.json

  echo -e "\n----------------------------"

  # Remove temporary JSON payload file
  rm payload.json
done < "$CSV"

echo "$ENTRY_DATE" >> "$LOG_FILE"