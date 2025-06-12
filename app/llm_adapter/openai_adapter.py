import asyncio
from typing import Dict, Optional
from dataclasses import dataclass

import openai
from openai import RateLimitError, APIError, APITimeoutError, APIConnectionError

from app.config.logging import setup_logger
from app.model.models import StyleEnum
from app.exception.custom_exceptions import LLMError, LLMRateLimitError, LLMTimeoutError

from .base import LLMAdapter

logger = setup_logger(__name__)

@dataclass
class OpenAIConfig:
    """Configuration for OpenAI adapter."""
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7
    max_retries: int = 3
    retry_delay: float = 1.0
    system_prompt: str = "You are a helpful writing assistant that rewrites text in different styles."

class OpenAIAdapter(LLMAdapter):
    """OpenAI LLM adapter using the OpenAI API."""

    def __init__(self, api_key: str, config: Optional[OpenAIConfig] = None):
        """Initialize the OpenAI adapter."""
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.config = config or OpenAIConfig()

        self.style_prompts: Dict[StyleEnum, str] = {
            StyleEnum.PIRATE: "Rewrite the following text in pirate speak with 'arrr', 'matey', etc.:",
            StyleEnum.HAIKU: "Rewrite the following text as a haiku (5-7-5 syllable pattern):",
            StyleEnum.FORMAL: "Rewrite the following text in a formal, professional tone:",
        }

    async def rewrite(self, text: str, style: StyleEnum) -> str:
        """Rewrite text using OpenAI's API with retries and error handling."""

        retry_count = 0

        while retry_count < self.config.max_retries:
            try:

                prompt = self.style_prompts.get(style)

                response = await self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {
                            "role": "system",
                            "content": self.config.system_prompt,
                        },
                        {"role": "user", "content": f"{prompt}\n\n{text}"},
                    ],
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                )

                return response.choices[0].message.content.strip()

            except RateLimitError as e:
                retry_count += 1
                if retry_count >= self.config.max_retries:
                    logger.error("Rate limit exceeded after retries", exc_info=True)
                    raise LLMRateLimitError("OpenAI rate limit exceeded") from e
                await self._wait_with_backoff(retry_count)
            except (APITimeoutError, APIConnectionError) as e:
                retry_count += 1
                if retry_count >= self.config.max_retries:
                    logger.error("API timeout/connection error after retries", exc_info=True)
                    raise LLMTimeoutError("OpenAI API timeout/connection error") from e
                await self._wait_with_backoff(retry_count)
            except APIError as e:
                logger.error("OpenAI API error", exc_info=True)
                raise LLMError(f"OpenAI API error: {str(e)}") from e 
            except Exception as e:
                logger.error("Unexpected error in OpenAI adapter", exc_info=True)
                raise LLMError(f"Unexpected error: {str(e)}") from e

    async def _wait_with_backoff(self, retry_count: int) -> None:
        """Wait with exponential backoff between retries."""
        delay = self.config.retry_delay * (2 ** (retry_count - 1))
        logger.info(f"Retrying in {delay} seconds... (attempt {retry_count + 1})")
        await asyncio.sleep(delay)
