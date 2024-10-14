# Local LLM with RAG and Speech Functionality on NVIDIA Jetson Orin

This repository contains all the necessary steps to set up a local large language model (LLM) with Retrieval-Augmented Generation (RAG) and speech functionality on an NVIDIA Jetson AGX Orin. The project has been developed as part of a university project by Theodor Stetter at the [RPTU](https://www.rptu.de/).

The project uses three main components:
1. The [**Ollama**](https://ollama.com/) container from the [Jetson Containers project](https://github.com/dusty-nv/jetson-containers) to run the LLM
2. [**NVIDIA Riva**](https://developer.nvidia.com/riva) for speech-to-text (ASR) and text-to-speech (TTS) capabilities
3. A custom **Python script** that runs the RAG, ASR, TTS and coordinates the user input and the corresponding outputs

## Requirements
- [NVIDIA Jetson AGX Orin](https://www.nvidia.com/de-de/autonomous-machines/embedded-systems/jetson-orin/) with JetPack [installed](https://developer.nvidia.com/embedded/learn/get-started-jetson-agx-orin-devkit)
- Internet connection to pull necessary models

## Project Setup

### 1. Ollama Container Setup

The [Ollama container](https://github.com/dusty-nv/jetson-containers/tree/master/packages/llm/ollama) is part of the Jetson Containers project by [Dustin Franklin](https://developer.nvidia.com/blog/author/dfranklin/). Follow these steps for the necessary adjustments on your Jetson device, and the installation of the Jetson Containers project.

#### a) Prerequisites

1. Follow the [System Setup](https://github.com/dusty-nv/jetson-containers/blob/master/docs/setup.md).
2. Clone the github repository and install the corresponding bash script.

```bash
git clone https://github.com/dusty-nv/jetson-containers
bash jetson-containers/install.sh
```

Refer to the Jetson Containers documentation for more detailed instructions if needed.
#### b) Starting the Ollama Container

Once the system setup is complete, run the following command to start the Ollama container:

```bash
jetson-containers run --name ollama $(autotag ollama)
```

#### c) Pull Required Models

After starting the container, you'll need to pull the necessary models (e.g., LLaMA 3 and Nomic Embed Text). Use the following commands in a new shell:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

Note: Ensure you have enough disk space available on your device, as these models can be quite large.

### 2. NVIDIA Riva Installation

NVIDIA Riva provides speech services like Automatic Speech Recognition (ASR) and Text-to-Speech (TTS). 

#### a) Prerequisites

1. Follow the [NVIDIA Riva Quickstart Guide](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/riva/resources/riva_quickstart_arm64) for installation on an ARM64 platform.
2. You can go through the [tutorials](https://github.com/nvidia-riva/python-clients#asr) to check for successful installation and operation of NVIDIA Riva

#### b) Starting Riva

After setting up Riva, navigate to the Riva Quickstart directory and run the shell script to start the Riva services. In the case of v2.16.0 this looks like this:

```bash

cd /mnt/riva_quickstart_arm64_v2.16.0
bash riva_start.sh
```
Note: Ensure that the correct path to your Riva directory is selected. If the Riva version changes, update the path accordingly.

### 3. Running the Python Script

The final step is running the Python script that integrates the Ollama and NVIDIA Riva services.
#### a) Installing Dependencies
It is recommended to use a virtual environment to install the packages and run the python script.

1. Setup the virtual environment
2. Install the necessary Python packages by running:
```
bash

pip install -r requirements.txt
```
Note: Ensure you are in the correct directory that contains the requirements.txt file.

#### b) Running the Script

To start the system, run the main Python script as follows:
```
bash

python3 RAG_n_RIVA.py
```

This script handles both the Retrieval-Augmented Generation (RAG) process using the Ollama model and the speech services provided by NVIDIA Riva.

## Troubleshooting and Common Issues

### Audio Playback Issues

If you are experiencing issues with audio input/output (e.g., using microphones or speakers), ensure that the Audio devices are selected in the system settings

### Model Download Issues

If model downloads fail or take too long, check your internet connection and available disk space. Some models, like llama3, are large, and the download may take some time.
Future Improvements


### Additional Information

For any additional help or information about the components used in this project, refer to their respective documentation:

    Ollama: Jetson Containers Documentation
    NVIDIA Riva: NVIDIA Riva Quickstart Guide
