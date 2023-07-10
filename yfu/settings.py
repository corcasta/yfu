import os
from pathlib import Path

PROJECT_PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")