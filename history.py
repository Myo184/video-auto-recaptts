from sheet import SheetManager
import pandas as pd
from config import SHEET_NAME

class HistoryManager:
    def __init__(self):
        self.sheet = SheetManager()
    
    def get_user_history(self, gmail, limit=50):
        try:
            history_sheet = self.sheet.client.open(SHEET_NAME).worksheet("History")
            records = history_sheet.get_all_records()
            
            user_history = [r for r in records if r.get("Email") == gmail]
            return user_history[-limit:]
        except:
            return []
    
    def get_all_history(self):
        try:
            history_sheet = self.sheet.client.open(SHEET_NAME).worksheet("History")
            return history_sheet.get_all_records()
        except:
            return []
    
    def get_stats(self):
        history = self.get_all_history()
        if not history:
            return {}
        
        df = pd.DataFrame(history)
        stats = {
            "total_videos": len(df),
            "unique_users": df["Email"].nunique(),
            "success_rate": (df["Status"] == "completed").mean() * 100,
            "daily_avg": len(df) / (df["Date"].nunique())
        }
        return stats
