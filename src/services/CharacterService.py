from llms.LlmComponent import ask_llm, get_llm, ask_llm_and_stream_response
from prompts.PromptLoader import load_character_builder_prompt

def init_character_creation(session_id):
    #  TODO : optimize/cache llm
    llm = get_llm(load_character_builder_prompt())
    # Initial message
    return ask_llm_and_stream_response(llm, session_id, "Игра началась!")

