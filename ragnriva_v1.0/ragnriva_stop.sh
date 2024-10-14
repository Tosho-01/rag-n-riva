#!/bin/bash

# Stop the ollama Docker container
echo "Stopping ollama container..."
docker stop ollama

# Navigate to the Riva directory and stop the Riva server
echo "Stopping Riva server..."
cd /mnt/riva_quickstart_arm64_v2.16.0 || { echo "Failed to change directory. Exiting."; exit 1; }
bash riva_stop.sh

echo "All processes have been stopped."
