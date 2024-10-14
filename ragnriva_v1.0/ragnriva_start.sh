#!/bin/bash


# Open the first terminal and start the ollama server
gnome-terminal --tab --title="Ollama Server" -- bash -c "sudo -n /usr/local/bin/jetson-containers run --name ollama \$(/usr/local/bin/autotag ollama)"

# Open the second terminal, change directory, and start the Riva server
gnome-terminal --tab --title="Riva Server" -- bash -c "cd /mnt/riva_quickstart_arm64_v2.16.0; bash riva_start.sh"

sleep 7

# Run the python script for ragnriva
gnome-terminal --tab --title="RAGnRIVA" -- bash -c "source /mnt/python-clients/venv/bin/activate; cd /mnt/Dokumente/VS_Code/ragnriva_v0.9/python_scripts; python3 main.py"

# Look at terminals with added "; exec bash" 		
