from __future__ import annotations

from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


load_dotenv()


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


llm = ChatOpenAI()


def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


checkpointer = MemorySaver()
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


def run_cli_chat(thread_id: str = "1") -> None:
    while True:
        user_message = input("Type here: ")
        print("User:", user_message)

        if user_message.strip().lower() in ["exit", "quit", "bye"]:
            break

        config = {"configurable": {"thread_id": thread_id}}
        response = chatbot.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
        )
        print("AI:", response["messages"][-1].content)


if __name__ == "__main__":
    run_cli_chat(thread_id="1")

