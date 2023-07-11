import os
from decouple import config
from pathlib import Path

# Root directory for easy calling
ROOT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

# List of required API keys 
OPENAI_API_KEY = config('OPENAI_API_KEY')
ELEVENLABS_API_KEY = config('ELEVENLABS_API_KEY')