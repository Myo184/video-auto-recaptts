from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle
import os
from sheet import SheetManager

class AuthManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
                       'https://www.googleapis.com/auth/userinfo.profile',
                       'openid']
        self.sheet = SheetManager()
        self.creds = None
    
    def login(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', self.SCOPES)
        creds = flow.run_local_server(port=0)
        
        user_info = self.get_user_info(creds)
        gmail = user_info['email']
        user = self.sheet.get_user(gmail)
        
        if not user:
            name = user_info.get('name', gmail.split('@')[0])
            self.sheet.create_user(gmail, name, member=False)
        
        return user_info
    
    def get_user_info(self, creds):
        import requests
        response = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            headers={'Authorization': f'Bearer {creds.token}'}
        )
        return response.json()
    
    def logout(self):
        self.creds = None
