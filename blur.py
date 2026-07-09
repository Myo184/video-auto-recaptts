import cv2
import numpy as np
from moviepy.editor import VideoFileClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os
from config import TEMP_FOLDER

class SubtitleBlurrer:
    def __init__(self):
        self.blur_amount = (51, 51)
        self.bottom_margin = 0.15
    
    def detect_subtitle_area(self, frame):
        height, width = frame.shape[:2]
        y_start = int(height * (1 - self.bottom_margin))
        roi = frame[y_start:height, 0:width]
        
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        subtitle_boxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > width * 0.3 and h > 20:
                subtitle_boxes.append((x, y + y_start, w, h))
        
        return subtitle_boxes
    
    def blur_frame(self, frame, boxes):
        if not boxes:
            return frame
        
        blurred = frame.copy()
        for (x, y, w, h) in boxes:
            roi = blurred[y:y+h, x:x+w]
            roi_blurred = cv2.GaussianBlur(roi, self.blur_amount, 0)
            blurred[y:y+h, x:x+w] = roi_blurred
        
        return blurred
    
    def process_video(self, video_path, output_path=None):
        if not output_path:
            output_path = os.path.join(TEMP_FOLDER, f"blurred_{os.path.basename(video_path)}")
        
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        subtitle_boxes = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % 30 == 0:
                subtitle_boxes = self.detect_subtitle_area(frame)
            
            blurred_frame = self.blur_frame(frame, subtitle_boxes)
            out.write(blurred_frame)
            
            frame_count += 1
        
        cap.release()
        out.release()
        
        return output_path
