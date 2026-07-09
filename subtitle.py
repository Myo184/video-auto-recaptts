from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import json
import os
from config import TEMP_FOLDER, DEFAULT_SUBTITLE_COLOR, DEFAULT_SUBTITLE_SIZE

class SubtitleGenerator:
    def __init__(self):
        self.color = DEFAULT_SUBTITLE_COLOR
        self.size = DEFAULT_SUBTITLE_SIZE
        self.position = "bottom"
    
    def generate_subtitle_clip(self, text, duration, position=None):
        if not position:
            position = self.position
        
        txt_clip = TextClip(
            text,
            fontsize=self.size,
            color=self.color,
            font='Arial',
            stroke_color='black',
            stroke_width=2,
            method='caption',
            size=(1920, None)
        )
        
        txt_clip = txt_clip.set_duration(duration)
        
        if position == "bottom":
            txt_clip = txt_clip.set_position(('center', 0.8), relative=True)
        elif position == "top":
            txt_clip = txt_clip.set_position(('center', 0.1), relative=True)
        elif position == "center":
            txt_clip = txt_clip.set_position(('center', 'center'), relative=True)
        
        return txt_clip
