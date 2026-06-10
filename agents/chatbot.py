from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

from prompts.healthcare_prompt import HEALTHCARE_PROMPT
from schemas.healthcare_response import HealthcareResponse

from typing import Optional

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    # structured_response: Optional[HealthcareResponse]

def chat_node(state: ChatState):
    messages = [
        SystemMessage(content=HEALTHCARE_PROMPT),
        *state["messages"]
    ]
    response = llm.invoke(messages)

    return {"messages": [response]}

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

workflow = graph.compile(checkpointer = checkpointer)

# Function for FastAPI
def get_chat_response(message: str, thread_id: str) -> str:
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    response = workflow.invoke({"messages": [HumanMessage(content=message)]},config=config)

    return response["messages"][-1].content