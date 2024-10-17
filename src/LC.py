from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from utils.jsonParser import parse_json
import os

# model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def load_character_builder_prompt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'roles', 'character_builder.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            load_character_builder_prompt(),
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
chain = prompt | model


with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages"
)

config = {"configurable": {"session_id": "abc2"}}


def stream_response(message):
    response=""
    for r in with_message_history.stream(
        {"messages": [HumanMessage(content=message)]},
        config=config,
    ):
        response +=r.content
        print(r.content, end='', flush=True)
    print()
    return response

# Initial message
stream_response("Игра началась!")

if __name__ == "__main__":
    answer = ""
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            parse_json(answer)
            break
        
        answer = stream_response(user_input)




# print(chain.invoke([HumanMessage(content="Hi! I'm Bob")]))
# print(chain.invoke([HumanMessage(content="What's my name?")]))