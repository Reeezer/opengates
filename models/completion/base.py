import os


class BaseCompletion:
    api_key: str
    model_name: str
    
    def __init__(self, api_key_env_var: str, model_name: str):
        self.api_key = os.getenv(api_key_env_var)
        self.model_name = model_name

    def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError
