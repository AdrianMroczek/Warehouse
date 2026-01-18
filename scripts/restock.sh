#!/bin/bash

# This script automates the process of restocking inventory items.

URL="http://127.0.0.1:8000/api/employee/products"

curl -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Nazwa", "price": 100.0, "quantity": 10, "category_id": 1 }'