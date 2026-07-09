# 🎬 Video Auto Recap SaaS

## Features
- ✅ Google OAuth Login
- ✅ Free User (2 videos/day)
- ✅ Member Subscription
- ✅ Gemini AI Summary
- ✅ Myanmar TTS
- ✅ Subtitle Generation
- ✅ Logo Overlay
- ✅ History Tracking
- ✅ API Key Rotation

## 🚀 Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/deploy?template=https://github.com/yourusername/video-recap-saas)

### Manual Deploy
1. Fork this repository
2. Go to https://railway.app
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose this repository
6. Add environment variables
7. Click "Deploy"

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| PORT | App port (default: 7860) | No |
| DEBUG | Debug mode (True/False) | No |
| SHEET_NAME | Google Sheet name | Yes |
| GOOGLE_SHEETS_CREDENTIALS_JSON | Google Sheets API credentials | Yes |
| GOOGLE_OAUTH_CREDENTIALS_JSON | Google OAuth credentials | Yes |
| GEMINI_MODEL | Gemini model name | No |
| FREE_DAILY_LIMIT | Free user daily limit | No |

## Local Development
```bash
git clone https://github.com/yourusername/video-recap-saas.git
cd video-recap-saas
pip install -r requirements.txt
python app.py
