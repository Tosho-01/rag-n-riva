"""
main.py
- coordinates the user interaction (inputs/outputs)
"""

# Initialization: Load USER_AGENT from .env file (for WebBaseLoader)
from dotenv import load_dotenv
load_dotenv()

# Imports
import animation
import time
from asr import ASR
from tts import TTS
from rag import load_or_create_project, create_chain

# Wait animation
wait = animation.Wait(text="Generating answer", animation='bar')

# Load database and retrieval chain
vector_db = load_or_create_project()
chain = create_chain(vector_db)

# Select text/audio modus
print("------- \nPlease select a mode \n1: text version \n2: audio version")
modus = input("Choose mode (number):")

# Text modus
if modus == '1' :
    print("-> text modus chosen")
    while True:
        # Question input
        questions = input('question: ')
        # Exit criterion
        if questions == 'exit':
            exit()
        # Generate response to question
        wait.start()
        response = chain.invoke(questions)
        wait.stop()
        # outputs answer
        print(response)

# Audio modus
elif modus == '2':
    print("-> audio modus chosen\n-----------------") 
    while True:
        # Question input
        print('Please ask your question into the microphone...')
        questions = ASR().strip()
        # Generate response to question
        wait.start()
        response = chain.invoke(questions)
        wait.stop()
        # outputs answer
        print('answer: '+response)
        TTS(response)