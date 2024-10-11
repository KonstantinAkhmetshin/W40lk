from langchain.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
import os

def get_language_model_gpt_4o_mini():
    # Ensure you have set the AIP_KEY environment variable
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    # Create the LLM instance using OpenAI's API with gpt-4o-mini
    # llm = OpenAI(
    #     api_key=openai_api_key,  # Use your AIP key
    #     model_name="gpt-4o-mini",  # Model name for GPT-4o-mini
    #     temperature=0.7,
    #     max_tokens=500
    # )
    return ChatOpenAI(model_name="gpt-4o-mini")