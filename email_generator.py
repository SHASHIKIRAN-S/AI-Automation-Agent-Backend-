import requests
import logging
from typing import Dict, Optional
from config import get_settings

logger = logging.getLogger(__name__)

class EmailGenerator:
    def __init__(self):
        self.settings = get_settings()

    def generate_email_content(self, prompt: str, tone: str = "friendly") -> Optional[str]:
        if not self.settings.email_api_ready:
            logger.warning("Email API not configured, using fallback")
            return None
        try:
            payload = {
                "prompt": f"Write a {tone} email about: {prompt}",
                "temperature": 0.7
            }
            headers = {
                "Authorization": f"Bearer {self.settings.email_api_key}"
            }
            response = requests.post(self.settings.email_api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            if "candidates" in data and data["candidates"]:
                return data["candidates"][0]["content"]["text"].strip()
            logger.warning(f"No content returned from Gemini API: {data}")
            return None
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return None

    def generate_email_with_subject(self, prompt: str, tone: str = "friendly") -> Dict[str, str]:
        content = self.generate_email_content(prompt, tone)
        if not content:
            # fallback email
            greeting = "Hi there," if tone.lower() in ["friendly","casual"] else "Dear Sir/Madam,"
            closing = "Best,\n[Your Name]" if tone.lower() in ["friendly","casual"] else "Best regards,\n[Your Name]"
            content = f"{greeting}\n\n{prompt}\n\n{closing}"
        first_line = content.strip().split("\n")[0]
        subject = first_line if len(first_line) < 80 else " ".join(prompt.split()[:7])
        return {"content": content, "subject": subject}
