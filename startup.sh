#!/bin/bash

echo "Testing the application..."

source .venv/bin/activate
cd ./src
python main.py > ../logs/test.log 2>&1

echo -e "\033[32mTest complete. Check the logs for details.\033[0m"