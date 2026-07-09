from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.video.fx.all import resize, crop
import speech_recognition as sr
import os
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER
from gemini import GeminiHandler
from tts import TTSEngine
from subtitle import SubtitleGenerator
from blur import SubtitleBlurrer
from logo import LogoManager
from sheet import SheetManager

class VideoProcessor:
    def __init__(self, gmail):
        self.gmail = gmail
        self.gemini = GeminiHandler()
        self.tts = TTSEngine()
        self.subtitle = SubtitleGenerator()
        self.blurrer = SubtitleBlurrer()
        self.logo_manager = LogoManager()
        self.sheet = SheetManager()
    
    def extract_audio(self, video_path):
        audio_path = os.path.join(TEMP_FOLDER, "extracted_audio.wav")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        video.close()
        return audio_path
    
    def speech_to_text(self, audio_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except:
                return None
    
    def process_video(self, video_path, logo_path=None, 
                      subtitle_color="#FFFFFF", 
                      subtitle_size=40,
                      subtitle_position="bottom",
                      logo_position="top-right",
                      logo_opacity=0.8):
        try:
            print("📤 Extracting audio...")
            audio_path = self.extract_audio(video_path)
            
            print("🎤 Converting speech to text...")
            transcript = self.speech_to_text(audio_path)
            if not transcript:
                return None, "Speech recognition failed"
            
            print("🤖 Generating summary with Gemini...")
            api_keys = self.sheet.get_user_api_keys(self.gmail)
            if not api_keys:
                return None, "No Gemini API keys found"
            self.gemini.set_keys(api_keys)
            
            summary = self.gemini.generate_summary(transcript)
            if not summary:
                return None, "Summary generation failed"
            
            print("🌏 Translating to Myanmar...")
            myanmar_text = self.gemini.translate_to_myanmar(summary)
            if not myanmar_text:
                myanmar_text = summary
            
            print("🔊 Generating Myanmar TTS...")
            tts_path = self.tts.generate_sync(myanmar_text)
            
            print("🎬 Processing video...")
            video = VideoFileClip(video_path)
            
            tts_audio = AudioFileClip(tts_path)
            video = video.set_audio(tts_audio)
            
            print("🌀 Blurring original subtitles...")
            blurred_video_path = self.blurrer.process_video(video_path)
            
            print("📝 Adding new subtitles...")
            self.subtitle.color = subtitle_color
            self.subtitle.size = subtitle_size
            self.subtitle.position = subtitle_position
            
            subtitle_clip = self.subtitle.generate_subtitle_clip(
                myanmar_text, 
                video.duration,
                subtitle_position
            )
            
            print("🖼️ Adding logo...")
            if logo_path and os.path.exists(logo_path):
                self.logo_manager.position = logo_position
                self.logo_manager.opacity = logo_opacity
                video = self.logo_manager.add_logo_to_video(video, logo_path)
            
            final_video = CompositeVideoClip([video, subtitle_clip])
            
            print("💾 Exporting final video...")
            output_path = os.path.join(OUTPUT_FOLDER, 
                                       f"final_{os.path.basename(video_path)}")
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                threads=4
            )
            
            video.close()
            final_video.close()
            
            self.sheet.log_history(
                self.gmail, 
                os.path.basename(video_path), 
                video.duration, 
                "completed"
            )
            
            print("✅ Video processing completed!")
            return output_path, "Success"
            
        except Exception as e:
            print(f"❌ Error in video processing: {e}")
            return None, str(e)
