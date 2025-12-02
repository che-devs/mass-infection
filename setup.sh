#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting setup..."

echo "Updating package manager and installing system packages..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

echo "Installing additional packages for audio..."
sudo apt-get install -y libasound-dev portaudio19-dev

echo "Creating and activating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setting environment variables..."
#export FLASK_APP=app.py

echo "Starting necessary services..."
#sudo service ... start 

echo "Setup completed successfully!"
