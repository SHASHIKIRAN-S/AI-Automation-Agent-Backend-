#!/usr/bin/env python3
"""
Environment Setup Script for AI Automation Agent

This script helps you set up the required environment variables for the application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Loads from .env in the same directory

smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")
smtp_user = os.getenv("SMTP_USERNAME")
smtp_pass = os.getenv("SMTP_PASSWORD")

def create_env_file():
    """Create a .env file with template values"""
    
    env_content = """# Email Generation API Configuration
# Get your API key from: https://platform.openai.com/api-keys
EMAIL_API_KEY=your-openai-api-key-here
EMAIL_API_URL=https://api.openai.com/v1/chat/completions

# SMTP Configuration for Gmail
# For Gmail, you need to:
# 1. Enable 2-factor authentication
# 2. Generate an App Password: https://myaccount.google.com/apppasswords
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com

# Optional SMTP Settings
SMTP_USE_TLS=true
SMTP_USE_SSL=false
SMTP_TIMEOUT=30
"""
    
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print(f"⚠️  .env file already exists at: {env_file}")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Setup cancelled")
            return False
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created .env file at: {env_file}")
        print("\n📝 Next steps:")
        print("1. Edit the .env file with your actual credentials")
        print("2. For Gmail: Enable 2FA and create an App Password")
        print("3. For OpenAI: Get your API key from https://platform.openai.com/api-keys")
        print("4. Test your configuration with: python test_smtp.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_configuration():
    """Check if the configuration is properly set up"""
    
    print("🔍 Checking configuration...")
    
    # Check if .env file exists
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Load environment variables
    from config import get_settings
    settings = get_settings()
    
    print(f"📧 Email API configured: {settings.email_api_configured}")
    print(f"📮 SMTP configured: {settings.smtp_configured}")
    
    if not settings.email_api_configured:
        print("⚠️  Email API not configured - emails will use basic templates")
    
    if not settings.smtp_configured:
        print("⚠️  SMTP not configured - cannot send emails")
        return False
    
    return True

def main():
    """Main setup function"""
    
    print("🚀 AI Automation Agent - Environment Setup")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Create .env file template")
        print("2. Check current configuration")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            create_env_file()
        elif choice == "2":
            check_configuration()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
