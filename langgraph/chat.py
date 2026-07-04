from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
from langchain.chat_models import init_chat_model

load_dotenv()

llm= init_chat_model(
    "gemini-2.5-flash",
    model_provider="google_genai"
)

class State(TypedDict):
    messages:Annotated[list, add_messages]

def chatbot(state: State):  #Node:just adds a text in pre-existing list
    response=llm.invoke(state.get("messages"))
    return {"messages":[response]}
    #print("Inside chatbot node",state)
    #return {"messages":["\n\nHi, this a message from Chatbot Node"]}

def samplenode(state: State):
    print("Inside sample node",state)
    return {"messages": ["\n\nSample Message Appended"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)  #We have to tell graph builder that chatbot is a node
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")         #START-->chatbot-->samplenode-->END
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)                #Edges

graph=graph_builder.compile()

updated_state=graph.invoke(State({"messages":["Hi,My name is Anurag"]}))
print("\n\nUpdated_state", updated_state)

#state={"messages": ["Hey there"]}
#node runs: chatbot(state:["Hey there"])->["Hi,this a message from the ChatBot node"])
#state={"messages": ["Hey there","Hi,this a message from the ChatBot node"]}

