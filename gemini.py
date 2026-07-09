import google.generativeai as genai
from sheet import SheetManager
import time

class GeminiHandler:
    def __init__(self):
        self.sheet = SheetManager()
        self.current_key_index = 0
        self.keys = []
    
    def set_keys(self, keys):
        self.keys = [k.strip() for k in keys if k.strip()]
        self.current_key_index = 0
    
    def get_next_key(self):
        if not self.keys:
            return None
        key = self.keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        return key
    
    def generate_summary(self, text, language="English"):
        attempts = 0
        max_attempts = len(self.keys) * 2
        
        while attempts < max_attempts:
            key = self.get_next_key()
            if not key:
                return None
            
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Summarize the following video transcript in {language}.
                Keep it concise (2-3 sentences) and highlight the key points.
                
                Transcript: {text}
                
                Summary:
                """
                
                response = model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                print(f"Error with API key {key}: {e}")
                attempts += 1
                time.sleep(1)
        
        return None
    
    def translate_to_myanmar(self, text):
        attempts = 0
        max_attempts = len(self.keys) * 2
        
        while attempts < max_attempts:
            key = self.get_next_key()
            if not key:
                return None
            
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Translate the following text to Myanmar (Burmese) language.
                Make sure it's natural and accurate.
                
                Text: {text}
                
                Myanmar Translation:
                """
                
                response = model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                print(f"Error with API key {key}: {e}")
                attempts += 1
                time.sleep(1)
        
        return None
