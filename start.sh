#!/bin/bash

echo "🚀 Starting Video Recap SaaS on Railway..."

# Set environment
export PORT=${PORT:-7860}
export RAILWAY=true

# Check if directories exist
mkdir -p uploads outputs temp

# Check for credentials
if [ ! -f "credentials.json" ]; then
    echo "⚠️  Warning: credentials.json not found!"
    echo "Please add Google Sheets credentials"
fi

if [ ! -f "client_secret.json" ]; then
    echo "⚠️  Warning: client_secret.json not found!"
    echo "Please add Google OAuth credentials"
fi

# Start the application
echo "✅ Application starting on port $PORT..."
python app.py
