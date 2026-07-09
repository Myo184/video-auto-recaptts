from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image
import numpy as np
import os
from config import DEFAULT_LOGO_POSITION, DEFAULT_LOGO_OPACITY, DEFAULT_LOGO_SIZE

class LogoManager:
    def __init__(self):
        self.position = DEFAULT_LOGO_POSITION
        self.opacity = DEFAULT_LOGO_OPACITY
        self.size = DEFAULT_LOGO_SIZE
    
    def resize_logo(self, logo_path, size=None):
        if not size:
            size = self.size
        
        img = Image.open(logo_path)
        img.thumbnail(size, Image.LANCZOS)
        temp_path = f"temp_logo_{os.path.basename(logo_path)}"
        img.save(temp_path)
        return temp_path
    
    def add_logo_to_video(self, video_clip, logo_path):
        resized_logo_path = self.resize_logo(logo_path)
        
        logo_clip = ImageClip(resized_logo_path, transparent=True)
        logo_clip = logo_clip.set_opacity(self.opacity)
        logo_clip = logo_clip.set_duration(video_clip.duration)
        
        if self.position == "top-left":
            pos = (20, 20)
        elif self.position == "top-right":
            pos = (video_clip.w - logo_clip.w - 20, 20)
        elif self.position == "bottom-left":
            pos = (20, video_clip.h - logo_clip.h - 20)
        elif self.position == "bottom-right":
            pos = (video_clip.w - logo_clip.w - 20, 
                   video_clip.h - logo_clip.h - 20)
        else:
            pos = (20, 20)
        
        logo_clip = logo_clip.set_position(pos)
        
        return CompositeVideoClip([video_clip, logo_clip])
