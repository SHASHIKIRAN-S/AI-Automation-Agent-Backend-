# Gmail App Password Setup Guide

## Issue
The SMTP test shows: `Application-specific password required`

This is expected behavior for Gmail accounts with 2-factor authentication enabled.

## Solution: Create an App Password

### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification" if not already enabled

### Step 2: Generate App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Scroll down to "2-Step Verification"
3. Click on "App passwords"
4. Select "Mail" as the app
5. Select "Other" as the device
6. Enter a name like "AI Automation Agent"
7. Click "Generate"
8. Copy the 16-character password

### Step 3: Update .env File
Replace the current password in your `.env` file:

```env
# Before
SMTP_PASSWORD=Shashi@2005!

# After (use the generated app password)
SMTP_PASSWORD=abcd efgh ijkl mnop
```

**Note:** Remove spaces from the app password when pasting it.

### Step 4: Test Again
Run the test script to verify the configuration:

```bash
python test_smtp.py
```

## Alternative: Use Less Secure Apps (Not Recommended)
If you don't want to use 2FA, you can enable "Less secure app access":
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "Less secure app access"
3. Use your regular password

**Warning:** This is less secure and may be disabled by Google.

## Security Best Practices
- ✅ Use App Passwords with 2FA
- ✅ Keep your app password secure
- ✅ Don't share app passwords
- ❌ Don't use regular passwords for SMTP
- ❌ Don't disable 2FA for convenience

## Troubleshooting
If you still have issues:
1. Make sure 2FA is enabled
2. Generate a new app password
3. Check that the password has no extra spaces
4. Verify the email address is correct
5. Try the test script again 