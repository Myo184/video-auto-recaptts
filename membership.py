from sheet import SheetManager
from datetime import datetime, timedelta
from config import FREE_DAILY_LIMIT

class MembershipManager:
    def __init__(self):
        self.sheet = SheetManager()
    
    def check_access(self, gmail):
        user = self.sheet.get_user(gmail)
        if not user:
            return False, "User not found"
        
        if self.sheet.is_member_valid(gmail):
            return True, "Member - Unlimited"
        
        if self.sheet.check_free_limit(gmail):
            return True, "Free User"
        
        return False, "Daily limit reached for free users"
    
    def process_video(self, gmail):
        user = self.sheet.get_user(gmail)
        if not user:
            return False
        
        if not self.sheet.is_member_valid(gmail):
            self.sheet.increment_today_count(gmail)
        
        return True
    
    def get_user_status(self, gmail):
        user = self.sheet.get_user(gmail)
        if not user:
            return None
        
        data = user["data"]
        is_member = data.get("Member") == "Yes"
        is_valid = self.sheet.is_member_valid(gmail)
        
        return {
            "gmail": data.get("Gmail"),
            "name": data.get("Name"),
            "member": is_member,
            "valid": is_valid,
            "remaining_days": self.sheet.get_remaining_days(gmail) if is_member else 0,
            "today_count": int(data.get("Today Count", 0)),
            "daily_limit": FREE_DAILY_LIMIT if not is_member else "Unlimited",
            "api_keys": self.sheet.get_user_api_keys(gmail)
        }
