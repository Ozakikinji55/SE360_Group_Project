#!/bin/bash

echo "Creating the Venv environment..."
python3 -m venv .venv
echo "Activating the Venv environment..."
source .venv/bin/activate
echo "Installing the required packages..." 
pip3 install -r requirements.txt
echo "Setup complete. You can now run the application."

