"""LLM client — talks to Gemini OR OpenAI, chosen by config.

Switch provider with two env vars (no code change):
    LLM_PROVIDER=gemini|openai
    LLM_API_KEY=<your key>

Kept separate from the detector so the detector never depends on a specific
SDK. The SDKs are synchronous, so calls run in a worker thread via
asyncio.to_thread to keep the FastAPI event loop free.
"""

from __future__ import annotations

import asyncio

from app.core.config import settings

PROVIDER_GEMINI = "gemini"
PROVIDER_OPENAI = "openai"


class LLMClient:
    """Async wrapper around Gemini / OpenAI."""

    def __init__(self) -> None:
        self._provider = settings.llm_provider
        self._model = settings.llm_model
        self._client = None

        # Import the SDK lazily so the app runs even when it's not installed
        # or no key is configured. Timeouts + tiny retry budgets keep the
        # firewall responsive instead of hanging on quota/network errors.
        if settings.has_llm_key:
            if self._provider == PROVIDER_OPENAI:
                from openai import OpenAI

                self._client = OpenAI(
                    api_key=settings.LLM_API_KEY,
                    timeout=settings.LLM_TIMEOUT_SECONDS,
                    max_retries=1,
                )
            else:
                from google import genai
                from google.genai import types

                http_options = types.HttpOptions(
                    timeout=settings.LLM_TIMEOUT_SECONDS * 1000,  # milliseconds
                    retry_options=types.HttpRetryOptions(
                        attempts=2, initial_delay=1.0, max_delay=4.0
                    ),
                )
                self._client = genai.Client(
                    api_key=settings.LLM_API_KEY, http_options=http_options
                )

    # ---- info ----
    @property
    def configured(self) -> bool:
        """True when an API key is present."""
        return self._client is not None

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def model(self) -> str:
        return self._model

    # ---- main entry point ----
    async def generate(self, prompt: str, system_instruction: str = "") -> str:
        """Send a prompt (+ optional system instruction) and return the text."""
        if self._client is None:
            raise RuntimeError("LLM client is not configured (missing API key).")

        if self._provider == PROVIDER_OPENAI:
            return await asyncio.to_thread(
                self._generate_openai, prompt, system_instruction
            )
        return await asyncio.to_thread(
            self._generate_gemini, prompt, system_instruction
        )

    # ---- provider-specific (sync, run in a thread) ----
    def _generate_gemini(self, prompt: str, system_instruction: str) -> str:
        kwargs: dict = {
            "model": self._model,
            "input": prompt,
            "generation_config": {
                "temperature": settings.LLM_TEMPERATURE,
                # Classification is simple: keep "thinking" low so calls are
                # fast and predictable (Gemini 3 enables thinking by default).
                "thinking_level": "low",
            },
        }
        if system_instruction:
            kwargs["system_instruction"] = system_instruction
        interaction = self._client.interactions.create(**kwargs)
        return interaction.output_text or ""

    def _generate_openai(self, prompt: str, system_instruction: str) -> str:
        messages: list[dict] = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=settings.LLM_TEMPERATURE,
        )
        return response.choices[0].message.content or ""
