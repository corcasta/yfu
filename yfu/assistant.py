import yaml
import speech_recognition as sr
import openai
from elevenlabs import generate, stream, set_api_key, voices
from settings import ROOT_DIR

class Impersonator():
    def __init__(self, 
                 brain: str = 'gpt-3.5-turbo', 
                 temperature: float = 0.5, 
                 category: str = 'anime', 
                 profile: str = 'tsundere', 
                 language: str = 'english',
                 monolingual: bool = True,
                 voice_id: str = 'OcoUoCWeJ3a3vNKOsjAz'):
        """_summary_

        Args:
            model (str, optional): _description_. Defaults to 'gpt-3.5-turbo'.
            temperature (float, optional): _description_. Defaults to 0.5.
            category (str, optional): _description_. Defaults to 'anime'.
            profile (str, optional): _description_. Defaults to 'tsundere'.
            language (str, optional): _description_. Defaults to 'english'.
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
        self.__character = {'role': 'system', 'content': personalities['archetype'][profile]}
        self.__recognizer = sr.Recognizer()
        
        # Chat history used for conversation based with context 
        self.history = [self.__character]
        
        
    def listen(self) -> None:
        """_summary_
        """
        with sr.Microphone() as source:
            self.__recognizer.adjust_for_ambient_noise(source, duration=1.5)
            print("Hey?")
            audio = self.__recognizer.listen(source)
            
            try:
                transcribed_audio = self.__recognizer.recognize_whisper(audio, self.__language)
                
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
                
            except sr.RequestError:
                print("Could not request results from Whisper")
                
            self.history.append({'role': 'user', 'content': transcribed_audio})
                
                
    def _reply(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        response = openai.ChatCompletion.create(model=self.__brain,
                                                temperature=self.__temperature,
                                                messages=self.history)
        
        content = response["choices"][0]["message"]["content"] 
        self.history.append({'role': 'assistant', 'content': content})
        return content
     
        
    def speak(self) -> None:
        """_summary_
        """
        content = self._reply()
        stream(generate(text=content,
                        voice=self.__voice_id,
                        model=self.__voice_model,
                        stream=True))
        