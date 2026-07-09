from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

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


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)  #We have to tell graph builder that chatbot is a node


graph_builder.add_edge(START, "chatbot")         #START-->chatbot-->samplenode-->END
graph_builder.add_edge("chatbot", END)                #Edges


def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
    

DB_URI="mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer=compile_graph_with_checkpointer(checkpointer=checkpointer)

    config = {
        "configurable": {
            "thread_id": "anurag"  #user_id
        }
    }
    '''updated_state=graph_with_checkpointer.invoke(
    State({"messages":["what is my name?"]}),
    config,
    )'''
    for chunk in graph_with_checkpointer.stream(
        State({"messages":["what am I learning"]}),
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
    

    #print("\n\nUpdated_state", updated_state)








#state={"messages": ["Hey there"]}
#node runs: chatbot(state:["Hey there"])->["Hi,this a message from the ChatBot node"])
#state={"messages": ["Hey there","Hi,this a message from the ChatBot node"]}

#Checkpointer(anurag)= hey, my name is anurag