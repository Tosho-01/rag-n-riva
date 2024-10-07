# Local LLM with RAG and Speech Functionality on NVIDIA Jetson Orin

This repository contains all the necessary steps to set up a local language model (LLM) with Retrieval-Augmented Generation (RAG) and speech functionality on an NVIDIA Jetson Orin. The project has been developed as part of a university project by Theodor Stetter at the [RPTU](https://www.rptu.de/).

The project uses three main components:
1. The **Ollama** container from the [Jetson Containers project](https://github.com/dusty-nv/jetson-containers)
2. **NVIDIA Riva** for speech-to-text (ASR) and text-to-speech (TTS) capabilities
3. A custom **Python script** that brings everything together

## Requirements
- **NVIDIA Jetson Orin** with JetPack installed
- **Docker** and **NVIDIA Container Toolkit** (Jetson already supports Docker-based environments)
- Internet connection to pull necessary models

## Project Setup

### 1. Ollama Container Setup

The Ollama container is provided by the [Jetson Containers project](https://github.com/dusty-nv/jetson-containers). Follow these steps to install and configure it:

#### a) System Setup

Run the following commands to install the necessary components for Jetson containers:

```bash
git clone https://github.com/dusty-nv/jetson-containers
bash jetson-containers/install.sh
```

Refer to the Jetson Containers setup documentation for more detailed instructions if needed.
#### b) Starting the Ollama Container

Once the system setup is complete, run the following command to start the Ollama container:

```bash
jetson-containers run --name ollama -v /mnt/ownFiles:/ownFiles $(autotag ollama)
```

This command starts the Ollama container, mounting /mnt/ownFiles from your local file system into the container.

#### c) Pull Required Models

After starting the container, you'll need to pull the necessary models (e.g., LLaMA 3 and Nomic Embed Text). Use the following commands inside the container:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

    Note: Ensure you have enough disk space available on your device, as these models can be quite large.

### 2. NVIDIA Riva Installation

NVIDIA Riva provides speech services like Automatic Speech Recognition (ASR) and Text-to-Speech (TTS). Follow the NVIDIA Riva Quickstart Guide for installation on an ARM64 platform.
#### a) Starting Riva

After setting up Riva, navigate to the Riva Quickstart directory and run the following commands to start the Riva services:

```bash

cd /mnt/riva_quickstart_arm64_v2.15.1
bash riva_start.sh
```
    Note: Ensure the Riva directory is mounted to your /mnt directory or the appropriate location where you've installed it. If the Riva version changes, update the path accordingly.

### 3. Running the Python Script

The final step is running the Python script that integrates the Ollama and NVIDIA Riva services.
#### a) Installing Dependencies

First, install the necessary Python packages by running:
```
bash

pip install -r requirements2.txt
```
       Note: Ensure you are in the correct directory that contains the requirements2.txt file.

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
