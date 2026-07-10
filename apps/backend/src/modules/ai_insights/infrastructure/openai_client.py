import logging
import os

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self) -> None:
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self._client = AsyncOpenAI(api_key=self._api_key, timeout=10.0) if self._api_key else None

    @property
    def is_configured(self) -> bool:
        return self._client is not None

    @property
    def model_name(self) -> str:
        return self._model

    async def generate(self, system_prompt: str, user_prompt: str) -> str | None:
        if not self.is_configured:
            logger.info("ai.openai_not_configured")
            return None
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )
            content = response.choices[0].message.content
            if response.usage:
                logger.info(
                    "ai.tokens_used",
                    extra={
                        "tokens_in": response.usage.prompt_tokens,
                        "tokens_out": response.usage.completion_tokens,
                        "model": self._model,
                    },
                )
            return content
        except Exception as e:
            logger.warning(f"ai.openai_error: {type(e).__name__}: {e}")
            return None
