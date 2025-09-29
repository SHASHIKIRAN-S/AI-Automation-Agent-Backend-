# Email Generation API Setup Guide

This guide explains how to configure the email generation API for your AI Automation Agent.

## Overview

The application now uses an external API service to generate email content instead of local LLM models. This provides:
- ✅ Better email quality and consistency
- ✅ No need to run local models
- ✅ Scalable and reliable service
- ✅ Multiple API providers supported

## Supported API Providers

### 1. OpenAI GPT (Recommended)
```env
EMAIL_API_KEY=sk-your-openai-api-key
EMAIL_API_URL=https://api.openai.com/v1/chat/completions
```

### 2. Anthropic Claude
```env
EMAIL_API_KEY=sk-ant-your-anthropic-api-key
EMAIL_API_URL=https://api.anthropic.com/v1/messages
```

### 3. Google Gemini
```env
EMAIL_API_KEY=your-gemini-api-key
EMAIL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
```

### 4. Custom API
```env
EMAIL_API_KEY=your-custom-api-key
EMAIL_API_URL=https://your-api-endpoint.com/generate
```

## Quick Setup

### Step 1: Get an API Key
1. **OpenAI**: Sign up at [platform.openai.com](https://platform.openai.com)
2. **Anthropic**: Sign up at [console.anthropic.com](https://console.anthropic.com)
3. **Google**: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Step 2: Update .env File
Edit your `.env` file and replace the placeholder:
```env
# Email Generation API
EMAIL_API_KEY=your-actual-api-key-here
EMAIL_API_URL=https://api.openai.com/v1/chat/completions
```

### Step 3: Test Configuration
```bash
# Check API status
curl http://localhost:8000/api-status

# Test email generation
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a professional email to schedule a meeting", "recipient": "test@example.com", "tone": "professional"}'
```

## API Configuration

### OpenAI Configuration
```env
EMAIL_API_KEY=sk-...
EMAIL_API_URL=https://api.openai.com/v1/chat/completions
```

### Anthropic Configuration
```env
EMAIL_API_KEY=sk-ant-...
EMAIL_API_URL=https://api.anthropic.com/v1/messages
```

### Custom API Configuration
If using a custom API, ensure it accepts:
- **Method**: POST
- **Headers**: `Authorization: Bearer <api_key>`, `Content-Type: application/json`
- **Body**: JSON with `prompt`, `tone`, `email_type`, `max_length`
- **Response**: JSON with `content` or `text` field

## Usage Examples

### Basic Email Generation
```python
from backend.email_generator import generate_email_content

# Generate email content
content = generate_email_content(
    prompt="Write a follow-up email after a meeting",
    tone="professional"
)
```

### Generate with Subject
```python
from backend.email_generator import generate_email_with_subject

# Generate both subject and content
email_data = generate_email_with_subject(
    prompt="Request for project update",
    tone="formal"
)

subject = email_data["subject"]
content = email_data["content"]
```

## Error Handling

The system includes comprehensive error handling:
- **API Key Missing**: Falls back to using prompt as content
- **API Unavailable**: Graceful degradation with fallback
- **Rate Limits**: Automatic retry with exponential backoff
- **Invalid Response**: Uses prompt as content

## Cost Considerations

- **OpenAI**: ~$0.002 per 1K tokens
- **Anthropic**: ~$0.008 per 1K tokens  
- **Google**: Free tier available, then pay-per-use

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** regularly
4. **Monitor API usage** to prevent unexpected charges
5. **Set up billing alerts** with your API provider

## Troubleshooting

### Common Issues

#### 1. "API key not configured"
- Check your `.env` file has the correct `EMAIL_API_KEY`
- Ensure no extra spaces or quotes around the key

#### 2. "API request failed"
- Verify your API key is valid
- Check the API URL is correct
- Ensure you have sufficient credits/quota

#### 3. "Unexpected API response format"
- The API response doesn't match expected format
- Check API documentation for correct response structure

### Debug Mode

Enable debug logging to see detailed API requests:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Migration from Local LLM

If you were previously using local LLM models:

1. **Remove local model files** (if any)
2. **Update your .env** with API credentials
3. **Test the new API** with a simple prompt
4. **Update frontend** if needed for new response format

## Support

For issues with API configuration:
1. Check the troubleshooting section above
2. Verify your API key and URL are correct
3. Test with a simple API call using curl or Postman
4. Check your API provider's documentation 