from typing import Literal

import dotenv
from google import genai

from models.completion.base import BaseCompletion


# https://ai.google.dev/gemini-api/docs/models

MODELS = Literal[
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
]


class GoogleCompletion(BaseCompletion):
    def __init__(self, api_key_env_var: str = "GOOGLE_API_KEY", model_name: MODELS = "gemini-2.5-flash"):
        super().__init__(api_key_env_var=api_key_env_var, model_name=model_name)

        # Initialize Google GenAI client
        self.client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text


if __name__ == "__main__":
    dotenv.load_dotenv()
    llm = GoogleCompletion()
    prompt = "What is the capital of France?"
    response = llm.generate(prompt)
    print(response)
