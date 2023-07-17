import yaml
import speech_recognition as sr
import openai
from elevenlabs import generate, stream
from settings import ROOT_DIR
from faster_whisper import WhisperModel

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


class Impersonator():
    def __init__(
        self, 
        brain: str = 'gpt-3.5-turbo',
        temperature: float = 0.5, 
        category: str = 'anime', 
        profile: str = 'tsundere', 
        language: str = 'english',
        monolingual: bool = True,
        voice_id: str = 'OcoUoCWeJ3a3vNKOsjAz'
        ):
        """_summary_

        Args:
            brain (str, optional): _description_. Defaults to 'gpt-3.5-turbo'.
            temperature (float, optional): _description_. Defaults to 0.5.
            category (str, optional): _description_. Defaults to 'anime'.
            profile (str, optional): _description_. Defaults to 'tsundere'.
            language (str, optional): _description_. Defaults to 'english'.
            monolingual (bool, optional): _description_. Defaults to True.
            voice_id (str, optional): _description_. Defaults to 'OcoUoCWeJ3a3vNKOsjAz'.
        """
        with open(ROOT_DIR + f'/personalities/{category}.yaml', 'r', encoding='utf-8') as source:
            try:
                personalities = yaml.safe_load(source)
            except yaml.YAMLError as exc:
                print(exc)    
        
        # Private attributes
        self.__brain = brain
        self.__temperature = temperature
        self.__language = language
        self.__voice_model = ('eleven_monolingual_v1' if monolingual else 'eleven_multilingual_v1')
        self.__voice_id = voice_id
        
        # Character used as reference for the chatbot
        self.__character = {'role': 'system', 'content': personalities['archetypes'][profile]}
        self.__recognizer = sr.Recognizer()
        
        # Chat history used for conversation based with context 
        self.history = [self.__character]
        
        self.__whisper = WhisperModel(model_size_or_path='large-v2', device="cpu", compute_type="int8")
        
        
    def listen(self) -> None:
        """_summary_
        """
        with sr.Microphone() as source:
            self.__recognizer.adjust_for_ambient_noise(source, duration=1.5)
            print("Hey?")
            audio = self.__recognizer.listen(source)
            
            try:
                transcribed_audio = self.__recognizer.recognize_whisper(audio, language=self.__language)
                
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
                
            except sr.RequestError:
                print("Could not request results from Whisper")
            
            print(f'You: {transcribed_audio}')    
            self.history.append({'role': 'user', 'content': transcribed_audio})
            
                
    def reply(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        response_data = openai.ChatCompletion.create(model=self.__brain,
                                                temperature=self.__temperature,
                                                messages=self.history)
        
        content = response_data["choices"][0]["message"]["content"] 
        self.history.append({'role': 'assistant', 'content': content})
        return content
     
        
    def speak(self) -> None:
        """_summary_
        """
        response = self.reply()
        stream(generate(text=response,
                        voice=self.__voice_id,
                        model=self.__voice_model,
                        stream=True))
        
        
class Conversation:
    def __init__(self, impersonator: Impersonator):
        self.__impersonator = impersonator
        
    def start(self, key_pressed):
        """_summary_

        Args:
            key_pressed (_type_): _description_
        """
        if key_pressed.char == 'z':
            self.__impersonator.listen()
            self.__impersonator.speak()
        