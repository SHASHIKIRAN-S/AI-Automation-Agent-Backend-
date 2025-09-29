#!/usr/bin/env python3
"""
SMTP Configuration Test Script

This script demonstrates the complete SMTP configuration and connection functionality.
Run this script to test your SMTP settings before using them in the main application.
"""

import os
import sys
from pathlib import Path
import smtplib
from config import get_settings
from mailer import send_email


def main():
    """Main test function"""
    print("🔧 SMTP Configuration Test")
    print("=" * 50)
    
    # Get settings
    try:
        settings = get_settings()
        print(f"✅ Settings loaded successfully")
        print(f"   SMTP Host: {settings.smtp_host}")
        print(f"   SMTP Port: {settings.smtp_port}")
        print(f"   Username: {settings.smtp_username}")
        print(f"   From Email: {settings.email_from}")
        print(f"   Use TLS: {settings.smtp_use_tls}")
        print(f"   Use SSL: {settings.smtp_use_ssl}")
        print(f"   Timeout: {settings.smtp_timeout}s")
    except Exception as e:
        print(f"❌ Error loading settings: {e}")
        return
    
    print("\n🔌 Testing SMTP Connection...")
    
    # Test sending a simple email
    print("\n📧 Testing Email Sending...")
    test_email = input("Enter a test email address (or press Enter to skip): ").strip()
    
    if test_email:
        success = send_email(
            to_email=test_email,
            subject="SMTP Configuration Test",
            content="This is a test email to verify your SMTP configuration is working correctly.\n\nIf you receive this email, your SMTP settings are properly configured!"
        )
        
        if success:
            print("✅ Test email sent successfully!")
        else:
            print("❌ Failed to send test email")
    else:
        print("⏭️  Skipping email test")

    # Test Gmail login
    print("\n🔧 Testing Gmail Login...")
    smtp_host = settings.smtp_host
    smtp_port = settings.smtp_port
    smtp_username = settings.smtp_username
    smtp_password = settings.smtp_password

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(smtp_username, smtp_password)
            print("Login successful!")
    except Exception as e:
        print("Login failed:", e)

    # Replace with your own test recipient email
    recipient = "your_test_email@gmail.com"
    subject = "SMTP Test Email"
    body = "This is a test email sent from the AI Automation Agent backend."

    try:
        send_email(recipient, subject, body)
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)


def create_env_template():
    """Create a template .env file"""
    env_template = """# SMTP Configuration
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
    
    env_file = Path(__file__).parent / ".env.template"
    with open(env_file, "w") as f:
        f.write(env_template)
    
    print(f"📄 Created .env template at: {env_file}")
    print("💡 Copy this file to .env and update with your actual settings")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--create-template":
        create_env_template()
    else:
        main() 