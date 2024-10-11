from .gpt_enum import GPT
from .gpt_4o_mini import get_language_model_gpt_4o_mini
from .gpt_j_6b import get_language_model_gpt_j_6b
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
import os

def load_character_builder_prompt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'roles', 'character_builder.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_character_builder_chain(llm):
    prompt_template = PromptTemplate(
        input_variables=[],
        template=load_character_builder_prompt()
    )
    return LLMChain(llm=llm, prompt=prompt_template)

def parse_json_from_response(response):
    try:
        json_start = response.rfind('{')
        json_end = response.rfind('}')
        if json_start != -1 and json_end != -1:
            return json.loads(response[json_start:json_end+1])
    except json.JSONDecodeError:
        pass
    return None

def get_qa_system(llmName: GPT):
    llm = get_language_model_gpt_j_6b() if llmName == GPT.GPT_J_6B else get_language_model_gpt_4o_mini()
    character_builder_chain = create_character_builder_chain(llm)

    def combined_qa(query):
        if query.lower() == "start character creation":
            character_creation_result = character_builder_chain.run()
            return {
                "character_creation": character_creation_result,
                "parsed_json": parse_json_from_response(character_creation_result)
            }
        else:
            return {"result": llm(query)}

    return combined_qa