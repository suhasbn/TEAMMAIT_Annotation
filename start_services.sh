#!/bin/bash

# Activate Conda environment
source /home/ec2-user/miniconda3/bin/activate prodigy_env

# Function to display stats
display_stats() {
    python - <<END
import json
from datetime import date, timedelta

STATS_FILE = '/home/ec2-user/annotation_stats.json'

def load_stats():
    try:
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"total_annotated": 0, "daily_stats": {}}

stats = load_stats()
today = str(date.today())
print("\nAnnotation Statistics:")
print(f"Total files annotated so far: {stats['total_annotated']}")
print(f"Files annotated today: {stats['daily_stats'].get(today, 0)}")
print(f"Files annotated this week: {sum(stats['daily_stats'].get(str(date.today() - timedelta(days=i)), 0) for i in range(7))}")
END
}

# Display stats at the start
display_stats

# Kill any existing processes
pkill -f "python /home/ec2-user/serve_media.py"
pkill -f "prodigy audio_annotation"

# Wait a moment for processes to terminate
sleep 2

echo "Starting Media Server..."
python /home/ec2-user/serve_media.py &

echo "Starting Prodigy..."
prodigy audio_annotation -F /home/ec2-user/updated_code.py audio_dataset &

# Save the PID of the last background process (Prodigy)
PRODIGY_PID=$!

# Wait a bit for Prodigy to start
sleep 5

echo "============================================="
echo "All services started successfully!"
echo "To begin annotating, open this URL in your web browser:"
echo "http://localhost:8080"
echo "If accessing from a different machine, replace 'localhost' with this instance's public IP or DNS."
echo "============================================="

# Function to handle stop signal
stop_services() {
    echo "Stopping services..."
    kill $PRODIGY_PID
    pkill -f "python /home/ec2-user/serve_media.py"
    wait $PRODIGY_PID
    display_stats
    exit 0
}

# Set up trap to catch SIGINT (Ctrl+C) and SIGTERM (sent by 'stop instance')
trap stop_services SIGINT SIGTERM

# Wait for Prodigy to finish
wait $PRODIGY_PID
