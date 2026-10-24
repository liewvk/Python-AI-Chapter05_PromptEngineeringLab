# ollama_service.py

from ollama import Client

from settings import (
    OLLAMA_HOST,
    MODEL_NAME,
    TIMEOUT_SECONDS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS
)


class OllamaService:

    def __init__(self):

        self.client = Client(
            host=OLLAMA_HOST,
            timeout=TIMEOUT_SECONDS
        )

    def generate(
        self,
        system_prompt,
        user_prompt,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
        json_schema=None
    ):
        """Generate a response using Ollama."""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        response = self.client.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=False,
            think=False,
            format=json_schema,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )

        answer = response.message.content or ""

        if not answer.strip():
            raise ValueError(
                "Ollama returned an empty response."
            )

        return answer.strip()
