from typing import Literal

import dotenv
from openai import OpenAI

from models.completion.base import BaseCompletion

# https://developers.openai.com/api/docs/models/

MODELS = Literal[
    "gpt-5.4-2026-03-05",
    "gpt-5.4-pro-2026-03-05",
    "gpt-5-mini-2025-08-07",
    "gpt-5-nano-2025-08-07",
    "gpt-5-2025-08-07",
    "gpt-4.1-2025-04-14",
]


class OpenAICompletion(BaseCompletion):
    def __init__(self, api_key_env_var: str = "OPENAI_API_KEY", model_name: MODELS = "gpt-5-2025-08-07"):
        super().__init__(api_key_env_var=api_key_env_var, model_name=model_name)

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model_name,
            input=prompt,
        )
        return response.text


if __name__ == "__main__":
    dotenv.load_dotenv()
    llm = OpenAICompletion()
    prompt = "What is the capital of France?"
    response = llm.generate(prompt)
    print(response)
