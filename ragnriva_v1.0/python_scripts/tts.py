"""
tts.py
- Utilizes the Text-to-Speech (TTS) from NVIDIA RIVA to synthesize speech from text
"""

# Imports
import time
import riva.client

# TTS function
def TTS(response):
    # Config
    auth = riva.client.Auth(uri='localhost:50051')
    service = riva.client.SpeechSynthesisService(auth)
    nchannels = 1
    sampwidth = 2
    sound_stream = riva.client.audio_io.SoundCallBack(
        output_device_index=None, nchannels=nchannels, sampwidth=sampwidth, framerate=44100)

    # Generate audio and measure the used time
    print("Generating audio for request...")
    start = time.time()

    resp = service.synthesize(
        text=response, voice_name="English-US.Female-1", language_code="en-US", sample_rate_hz=44100,
        quality=20
    )
    stop = time.time()
    sound_stream(resp.audio)
