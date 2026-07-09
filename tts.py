import edge_tts
import asyncio
import uuid
from config import TEMP_FOLDER
import os

class TTSEngine:
    def __init__(self):
        self.voice = "my-MY-NandarNeural"
        
    async def generate_audio(self, text, output_path=None):
        if not output_path:
            output_path = os.path.join(TEMP_FOLDER, f"tts_{uuid.uuid4()}.mp3")
        
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        return output_path
    
    def generate_sync(self, text):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.generate_audio(text))
