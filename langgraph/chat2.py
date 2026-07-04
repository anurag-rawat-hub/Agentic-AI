from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Optional, Literal
from google import genai
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(
    api_key=api_key
)

class State(TypedDict):
    user_query: str
    lm_output: Optional[str]
    is_good:Optional[bool]

def chatbot(state: State):
    print("chatbot node")
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=state["user_query"]
)
    state["lm_output"]=response.text
    return state


#Conditional edge

def evaluate_response(state:State) -> Literal["chatbot_gemini","endnode"]:
    print("condtional node")
    if False:
        return "endnode"
    return "chatbot_gemini"

def chatbot_gemini(state: State):
    print("chatbot_gemini node")
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=state["user_query"]
)
    state["lm_output"]=response.text
    return state

def endnode(state:State):
    print("endnode")
    return state


grapgh_builder=StateGraph(State)

grapgh_builder.add_node("chatbot", chatbot)
grapgh_builder.add_node("chatbot_gemini", chatbot_gemini)
grapgh_builder.add_node("endnode", endnode)

grapgh_builder.add_edge(START,"chatbot")
grapgh_builder.add_conditional_edges("chatbot",evaluate_response)
grapgh_builder.add_edge("chatbot_gemini","endnode")
grapgh_builder.add_edge("endnode",END)

graph=grapgh_builder.compile()

updated_state=graph.invoke(State({"user_query":"Hey, What is 2+3?"}))
print(updated_state)
