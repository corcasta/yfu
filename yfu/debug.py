import os
import yaml
from settings import ROOT_DIR, OPENAI_API_KEY, GOOGLE_APPLICATION_CREDENTIALS


"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS


import os
import shutil
import subprocess
from pathlib import Path

def is_installed(lib_name: str) -> bool:
    lib = shutil.which(lib_name)
    if lib is None:
        return False
    global_path = Path(lib)
    # else check if path is valid and has the correct access rights
    return global_path.exists() and os.access(global_path, os.X_OK)

    
def play(audio: bytes, notebook: bool = False) -> None:
    if notebook:
        from IPython.display import Audio, display

        display(Audio(audio, rate=44100, autoplay=True))
    else:
        if not is_installed("ffplay"):
            raise ValueError("ffplay from ffmpeg not found, necessary to play audio.")
        args = ["ffplay", "-autoexit", "-", "-nodisp"]
        proc = subprocess.Popen(
            args=args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate(input=audio)
        proc.poll()
        

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="""
                                              It's difficult to provide an exact average for the number of words spoken by a human per month because it can vary greatly depending on various factors such as age, occupation, social interactions, and personal characteristics. However, I can provide you with a rough estimate based on some available data. 
                                              On average, adults speak at a rate of about 125 to 150 words per minute during a conversation. Assuming an average conversation lasts for about 30 minutes, we can estimate that an adult may speak around 3,750 to 4,500 words per conversation.
                                              """)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
play(audio=response.audio_content)

#with open("output.mp3", "wb") as out:
#    # Write the response to the output file.
#    out.write(response.audio_content)
#    print('Audio content written to file "output.mp3"')