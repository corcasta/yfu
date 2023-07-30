import openai
from pynput import keyboard
from elevenlabs import set_api_key
from settings import OPENAI_API_KEY, ELEVENLABS_API_KEY
from assistant import Impersonator, Conversation


def main():    
    openai.api_key = OPENAI_API_KEY
    set_api_key(ELEVENLABS_API_KEY)
    
    marin = Impersonator(profile='yandere')
    conversation = Conversation(marin)
    
    while True:
        with keyboard.Listener(on_press=conversation.start) as listener:
            listener.join()

        
if __name__ == "__main__":
    main()
