import os

from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

gemini_model_client = OpenAIChatCompletionClient(
    api_key=gemini_api_key,
    model="gemini-2.5-flash-lite",
    model_info={
        "family": "google",
        "vision": True,
        "json_output": False,
        "function_calling": True,
        "structured_output": True,
    }
)

ollama_client = OllamaChatCompletionClient(model="llama3.1")

# ollama_client = OllamaChatCompletionClient(model="llama3.2-vision")