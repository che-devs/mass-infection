#!/bin/bash

echo "Navigating to the project directory..."
cd ~/mass-infection/

echo "Activating the virtual environment..."
source .venv/bin/activate

echo "Starting the main Python application..."
python3 main.py
