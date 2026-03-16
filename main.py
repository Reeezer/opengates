import dotenv

from opengates.messages.user import UserMessage
from opengates.models.completion.google import GoogleCompletion

if __name__ == "__main__":
    dotenv.load_dotenv()
    llm = GoogleCompletion()
    history = UserMessage(content="What is the capital of France?")
    response = llm.generate(history)
    print(response)
