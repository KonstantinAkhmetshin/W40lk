from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from storage.SessionStorage import get_session_history

def get_llm(systemPrompt):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            systemPrompt,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
    )
    chain = prompt | model

    llm = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="messages"
    )
    return llm


def ask_llm(llm: RunnableWithMessageHistory, sessionId, message):
    response = llm.invoke(
        {"messages": [HumanMessage(content=message)]},
        config={"configurable": {"session_id": sessionId}},
    )
    return response.content

def ask_llm_and_stream_response(llm: RunnableWithMessageHistory, sessionId, message):
    for r in llm.stream(
        {"messages": [HumanMessage(content=message)]},
        config={"configurable": {"session_id": sessionId}},
    ):
        yield r.content
