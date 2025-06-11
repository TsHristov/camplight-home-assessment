from typing import Dict

import openai

from app.config.logging import setup_logger
from app.model.models import StyleEnum

from .base import LLMAdapter

logger = setup_logger(__name__)


class OpenAIAdapter(LLMAdapter):
    """OpenAI LLM adapter using the OpenAI API."""

    def __init__(self, api_key: str, model="gpt-3.5-turbo"):
        """Initialize the OpenAI adapter."""
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

        self.style_prompts: Dict[StyleEnum, str] = {
            StyleEnum.PIRATE: "Rewrite the following text in pirate speak with 'arrr', 'matey', etc.:",
            StyleEnum.HAIKU: "Rewrite the following text as a haiku (5-7-5 syllable pattern):",
            StyleEnum.FORMAL: "Rewrite the following text in a formal, professional tone:",
        }

    async def rewrite(self, text: str, style: StyleEnum) -> str:
        """Rewrite text using OpenAI's API."""

        try:
            prompt = self.style_prompts.get(style)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful writing assistant that rewrites text in different styles.",
                    },
                    {"role": "user", "content": f"{prompt}\n\n{text}"},
                ],
                max_tokens=500,
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(
                "Got an error while calling OpenAI API, details: %s",
                str(e),
                exc_info=True,
            )
            raise e
