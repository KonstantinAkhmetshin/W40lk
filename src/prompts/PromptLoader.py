import os

def load_character_builder_prompt():
    return load_prompt_by_name("character_builder.txt")

def load_game_master_prompt():
    return load_prompt_by_name("game_master.txt")

def load_prompt_by_name(promptName):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, promptName)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()