#!/bin/bash

set -e

# Function to check if port is in use
check_port() {
    sudo lsof -i :8090 >/dev/null 2>&1
}

# Activate the Conda environment
source /home/ec2-user/miniconda3/bin/activate prodigy_old

# Kill any process using port 8090
while check_port; do
    echo "Port 8090 is in use. Attempting to kill the process..."
    sudo fuser -k 8090/tcp || true
    sleep 2
done

# Verify port is free
if check_port; then
    echo "Port 8090 is still in use. Exiting."
    exit 1
else
    echo "Port 8090 is free."
fi

# Set environment variable for the port
export PRODIGY_PORT=8090

# Start Prodigy in the background
echo "Starting Prodigy..."
nohup prodigy audio_annotation -F /home/ec2-user/updated_code.py audio_dataset > prodigy.log 2>&1 &

# Keep the shell interactive
echo "Prodigy service started. Head over to http://10.65.201.85:8090"
echo "To stop Prodigy, use 'sudo fuser -k 8090/tcp' to kill the process."
echo "Type 'exit' to close the SSH session."

# Start an interactive shell
exec bash --login
