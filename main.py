import os
import openai
from pynput import keyboard
import speech_recognition as sr
from elevenlabs import generate, play, set_api_key, voices

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
KEYWORD = "hey"
chat_history = [] # Empty history at the beginning



def personal_assistant(key):
    #print("Tecla: ", str(key,char) == "z")
    if key.char == 'z':
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1.5)
            print("What's up?")
            audio = r.listen(source)

            # recognize speech using whisper
            try:
                petition = r.recognize_whisper(audio, language="english")
                print("Whisper thinks you said: \n " + petition)
                print("")
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Whisper")
            
            chat_history.append()
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                    temperature=0.5,
                                                    messages=[
,
                                                        {
                                                            "role": "user", 
                                                            "content": petition
                                                        }
                                                    ])
            
            # OpenAI reposne
            response_text = response["choices"][0]["message"]["content"]  
            audio_audio = generate(text=response_text,
                                voice="OcoUoCWeJ3a3vNKOsjAz",
                                model="eleven_monolingual_v1")
            
            print(response_text)
            play(audio_audio)


def main():    
    openai.api_key = OPENAI_API_KEY
    set_api_key(ELEVENLABS_API_KEY)
    
    while True:
        with keyboard.Listener(on_press=personal_assistant) as listener:
            listener.join()
            
            

    
    #audio_text = r.recognize_whisper_api(audio_data=audio, api_key=OPENAI_API_KEY)
    #print(f"You mentioned: {audio_text}")
        
        
        
if __name__ == "__main__":
    main()