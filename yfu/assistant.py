import yaml
import speech_recognition as sr
from settings import PROJECT_PATH

class Impersonator():
    def __init__(self, model, temperature, category: str = 'anime', profile: str = 'tsundere', language: str = 'english'):
        """_summary_

        Args:
            category (str, optional): _description_. Defaults to 'anime'.
            profile (str, optional): _description_. Defaults to 'tsundere'.
            language (str, optional): _description_. Defaults to 'english'.
        """
        with open(PROJECT_PATH + f'/personalities/{category}.yaml', 'r', encoding='utf-8') as source:
            try:
                personalities = yaml.safe_load(source)
            except yaml.YAMLError as exc:
                print(exc)    
        
        # Character used as reference for the chatbot
        self.__character = {'role': 'system', 'content': personalities['archetype'][profile]}
        self.__recognizer = sr.Recognizer()
        
        # Chat history used for conversation based with context 
        self.history = [self.__character]
        
        
    def listen(self) -> None:
        with sr.Microphone() as source:
            self.__recognizer.adjust_for_ambient_noise(source, duration=1.5)
            print("Hey?")
            audio = self.__recognizer.listen(source)
            
            try:
                transcribed_audio = self.__recognizer.recognize_whisper(audio, language)
                
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
                
            except sr.RequestError:
                print("Could not request results from Whisper")
                
            self.history.append({'role': 'user', 'content': transcribed_audio})
                
            