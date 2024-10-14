"""
asr.py
- Utilizes the automated speech recognition (ASR) from NVIDIA RIVA to transcribe the microphone input into text
- Enables speech processing based on activation/stop/exit words
- Determines the end of a question through the recognition of puntuations
"""

# Imports
import sys
import string
sys.path.append('/mnt/python-clients')
import riva.client
import riva.client.audio_io 
import sounddevice                      # fixes warnings from riva

# Variables
is_active = False
questions = ""

# Checks the transcripted text for punctuation to determine the end of the question
def check_punctuation(questions):
    return any(char in string.punctuation for char in questions)

# Set Activation/Stop Word to enable/disable the processing of audio input
def detect_activation_word(transcript, activation_word="start", stop_word="stop"):
    global is_active
    if activation_word in transcript.lower():
        print("Activation word detected. Starting transcription...")
        is_active=True
        return transcript.lower().replace(activation_word, "").strip()
    elif stop_word in transcript.lower():
        print("Stop word detected. Stopping transcription...")
        is_active=False
        return transcript.lower().replace(stop_word, "").strip()
    return transcript

# Set Exit Word to exit the program
def detect_exit_word(transcript, exit_word="exit"):
    if exit_word in transcript.lower():
        print("Exit word detected. Exiting program...")
        sys.exit()
    return transcript

# The automated speech recognition (ASR) from NVIDIA RIVA to transcribe the microphone input into text
def ASR():
    # Config
    auth = riva.client.Auth(uri='localhost:50051')          # Authentification/ RIVA-Server adress
    asr_service = riva.client.ASRService(auth)
    config = riva.client.StreamingRecognitionConfig(        
        config=riva.client.RecognitionConfig(
            encoding=riva.client.AudioEncoding.LINEAR_PCM,  
            language_code="en-US",                          # Language
            max_alternatives=1,
            profanity_filter=False,                         # Profanity Filter
            enable_automatic_punctuation=True,              # Automatic Punctuation
            verbatim_transcripts=not False,
            sample_rate_hertz=16000,
            audio_channel_count=1,
        ),
        interim_results=True,
    )
    riva.client.add_word_boosting_to_config(config, boosted_lm_words=None, boosted_lm_score=4.0)
    riva.client.add_endpoint_parameters_to_config(
        config, 
        start_history=-1,           # Value to detect and initiate start of speech utterance
        start_threshold=-1.0,       # Threshold value for detecting the start of speech utterance
        stop_history=-1,            # Value to reset the endpoint detection history
        stop_history_eou=-1,        # Value to determine the response history for endpoint detection
        stop_threshold=-1.0,        # Threshold value for detecting the end of speech utterance
        stop_threshold_eou=-1.0     # Threshold value 
    )

    # Variables
    global is_active
    global questions

    # Audio processing
    with riva.client.audio_io.MicrophoneStream(rate=16000, chunk=1600, device=None) as audio_chunk_iterator:
        for response in asr_service.streaming_response_generator(audio_chunks=audio_chunk_iterator, streaming_config=config):
            if response.results and response.results[0].is_final:
                transcript = response.results[0].alternatives[0].transcript
                print(f"Detected speech: {transcript}")

                # Check transcript for Activation/Stop/Exit word
                detect_exit_word(transcript)
                transcript = detect_activation_word(transcript)

                if is_active:
                    questions = transcript
                    if check_punctuation(questions):
                        print(f"Final transcription: {questions.strip()}")
                        break
                else:
                    print('The speech recognition is not active (say "start")')

    return questions.strip()
