# SMTP Configuration Guide

This guide explains how to configure SMTP settings for the AI Automation Agent email functionality.

## Overview

The application includes a complete SMTP configuration system with:
- ✅ Environment-based configuration
- ✅ Connection pooling and management
- ✅ Support for SSL/TLS encryption
- ✅ Comprehensive error handling
- ✅ Configuration validation
- ✅ Connection testing

## Quick Setup

### 1. Create Environment File

Copy the template and configure your settings:

```bash
# Create .env file from template
python test_smtp.py --create-template
cp .env.template .env
```

### 2. Configure SMTP Settings

Edit the `.env` file with your email provider settings:

```env
# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com

# Optional SMTP Settings
SMTP_USE_TLS=true
SMTP_USE_SSL=false
SMTP_TIMEOUT=30
```

### 3. Test Configuration

Run the test script to verify your settings:

```bash
python test_smtp.py
```

## Email Provider Settings

### Gmail
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```
**Note:** Use an App Password instead of your regular password.

### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### Yahoo
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### Custom SMTP Server
```env
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

## Configuration Options

### Required Settings
- `SMTP_HOST`: SMTP server hostname
- `SMTP_PORT`: SMTP server port (25, 465, or 587)
- `SMTP_USERNAME`: Your email username
- `SMTP_PASSWORD`: Your email password or app password
- `EMAIL_FROM`: The "from" email address

### Optional Settings
- `SMTP_USE_TLS`: Enable TLS encryption (default: true)
- `SMTP_USE_SSL`: Enable SSL encryption (default: false)
- `SMTP_TIMEOUT`: Connection timeout in seconds (default: 30)

## Usage Examples

### Basic Email Sending
```python
from config import send_email

# Send a simple text email
success = send_email(
    to_email="recipient@example.com",
    subject="Test Email",
    content="This is a test email."
)
```

### HTML Email with CC/BCC
```python
from config import send_email

# Send HTML email with CC and BCC
success = send_email(
    to_email="recipient@example.com",
    subject="HTML Test Email",
    content="<h1>Hello!</h1><p>This is an HTML email.</p>",
    content_type="html",
    cc=["cc@example.com"],
    bcc=["bcc@example.com"],
    reply_to="reply@example.com"
)
```

### Test Connection
```python
from config import test_smtp_connection, validate_smtp_config

# Test SMTP connection
if test_smtp_connection():
    print("SMTP connection successful!")

# Validate configuration
validation = validate_smtp_config()
if validation["valid"]:
    print("Configuration is valid")
else:
    print("Configuration errors:", validation["errors"])
```

## Troubleshooting

### Common Issues

#### 1. Authentication Failed
- **Cause**: Incorrect username/password
- **Solution**: Verify credentials and use app passwords for Gmail

#### 2. Connection Timeout
- **Cause**: Firewall blocking SMTP port
- **Solution**: Check firewall settings and try different ports

#### 3. SSL/TLS Errors
- **Cause**: Incorrect encryption settings
- **Solution**: Verify port and encryption settings match your provider

#### 4. "Less Secure App" Error (Gmail)
- **Cause**: Gmail blocking less secure apps
- **Solution**: Enable 2FA and use App Passwords

### Debug Mode

Enable debug logging by modifying the logging level in `config.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Testing Commands

```bash
# Test configuration
python test_smtp.py

# Create environment template
python test_smtp.py --create-template

# Validate settings only
python -c "from config import validate_smtp_config; print(validate_smtp_config())"
```

## Security Best Practices

1. **Use App Passwords**: For Gmail and other providers that support them
2. **Environment Variables**: Never hardcode credentials in code
3. **Encryption**: Always use TLS/SSL when available
4. **Timeouts**: Set reasonable connection timeouts
5. **Validation**: Always validate configuration before use

## API Reference

### Functions

#### `send_email(to_email, subject, content, content_type="plain", cc=None, bcc=None, reply_to=None)`
Send an email with comprehensive error handling.

#### `test_smtp_connection() -> bool`
Test SMTP connection and authentication.

#### `validate_smtp_config() -> dict`
Validate SMTP configuration and return detailed status.

#### `get_settings() -> Settings`
Get application settings with caching.

### Classes

#### `SMTPConnection`
Context manager for SMTP connections with automatic cleanup.

#### `Settings`
Pydantic settings class with validation for all SMTP configuration.

## Migration from Legacy Code

The new SMTP system is backward compatible. If you have existing code using the old `send_email` function, it will continue to work:

```python
# Old way (still works)
from config import send_simple_email
from email.mime.text import MIMEText

msg = MIMEText("Hello")
msg["Subject"] = "Test"
msg["From"] = "from@example.com"
msg["To"] = "to@example.com"

send_simple_email(msg)
```

## Support

For issues with SMTP configuration:
1. Check the troubleshooting section above
2. Run the test script to identify specific problems
3. Review your email provider's SMTP documentation
4. Check the application logs for detailed error messages 