"""
LLM Client for interacting with OpenRouter API.
"""

import requests
import logging
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL

logger = logging.getLogger(__name__)

class OpenRouterLLMClient:
    """
    Handles communication with the OpenRouter LLM API.
    """

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str = OPENROUTER_API_KEY, model: str = OPENROUTER_MODEL):
        self.api_key = api_key
        self.model = model

    def generate_email(self, prompt: str) -> str:
        """
        Generate email content using the LLM.

        Args:
            prompt: Text prompt to send to the model.

        Returns:
            Generated content as a string.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=body,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API request failed: {e}")
            raise
