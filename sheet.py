import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd
from config import GOOGLE_SHEETS_CREDENTIALS, SHEET_NAME, FREE_DAILY_LIMIT

class SheetManager:
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            GOOGLE_SHEETS_CREDENTIALS, scope
        )
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(SHEET_NAME).sheet1
        
        if not self.sheet.get_all_values():
            headers = ["Gmail", "Name", "Member", "Expire", 
                      "Today Count", "Last Reset", "API Keys", "Status"]
            self.sheet.append_row(headers)
    
    def get_user(self, gmail):
        records = self.sheet.get_all_records()
        for idx, record in enumerate(records, start=2):
            if record.get("Gmail") == gmail:
                return {"row": idx, "data": record}
        return None
    
    def create_user(self, gmail, name, member=False):
        today = datetime.now().strftime("%Y-%m-%d")
        row = [gmail, name, "Yes" if member else "No", 
               "", "0", today, "", "active"]
        self.sheet.append_row(row)
    
    def update_user(self, row, column, value):
        col_map = {"Gmail": 1, "Name": 2, "Member": 3, "Expire": 4,
                   "Today Count": 5, "Last Reset": 6, "API Keys": 7, "Status": 8}
        self.sheet.update_cell(row, col_map[column], value)
    
    def get_user_api_keys(self, gmail):
        user = self.get_user(gmail)
        if user:
            keys_str = user["data"].get("API Keys", "")
            return [k.strip() for k in keys_str.split(",") if k.strip()]
        return []
    
    def set_user_api_keys(self, gmail, keys):
        user = self.get_user(gmail)
        if user:
            self.update_user(user["row"], "API Keys", ",".join(keys))
    
    def check_free_limit(self, gmail):
        user = self.get_user(gmail)
        if not user:
            return False
        
        data = user["data"]
        today = datetime.now().strftime("%Y-%m-%d")
        
        if data.get("Last Reset") != today:
            self.update_user(user["row"], "Today Count", "0")
            self.update_user(user["row"], "Last Reset", today)
            return True
        
        if data.get("Member") == "Yes":
            return True
        
        count = int(data.get("Today Count", 0))
        if count < FREE_DAILY_LIMIT:
            return True
        
        return False
    
    def increment_today_count(self, gmail):
        user = self.get_user(gmail)
        if user:
            count = int(user["data"].get("Today Count", 0))
            self.update_user(user["row"], "Today Count", str(count + 1))
    
    def is_member_valid(self, gmail):
        user = self.get_user(gmail)
        if not user:
            return False
        
        data = user["data"]
        if data.get("Member") != "Yes":
            return False
        
        expire_str = data.get("Expire")
        if not expire_str:
            return False
        
        expire_date = datetime.strptime(expire_str, "%Y-%m-%d")
        return expire_date > datetime.now()
    
    def get_remaining_days(self, gmail):
        user = self.get_user(gmail)
        if not user:
            return 0
        
        expire_str = user["data"].get("Expire")
        if not expire_str:
            return 0
        
        expire_date = datetime.strptime(expire_str, "%Y-%m-%d")
        remaining = (expire_date - datetime.now()).days
        return max(0, remaining)
    
    def log_history(self, gmail, video_name, duration, status):
        try:
            history_sheet = self.client.open(SHEET_NAME).worksheet("History")
            row = [gmail, video_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   str(duration), status]
            history_sheet.append_row(row)
        except Exception as e:
            print(f"History log error: {e}")
