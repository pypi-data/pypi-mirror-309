import streamlit as st
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseMessage, HumanMessage, AIMessage

# Define the state of our graph
class GraphState(TypedDict):
    messages: List[BaseMessage]
    next: str

# Define our agents
def create_agent(name: str, system_message: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}"),
    ])
    return prompt | ChatOllama(model="llama3.2:3b")

researcher = create_agent(
    "Researcher",
    "You are a research agent. Your job is to find relevant information about the given topic."
)

writer = create_agent(
    "Writer",
    "You are a writer agent. Your job is to take the research provided and create a concise summary."
)

# Define node functions
def researcher_node(state: GraphState) -> GraphState:
    messages = state['messages']
    response = researcher.invoke({"input": messages[-1].content})
    return {
        "messages": messages + [AIMessage(content=response.content)],
        "next": "writer"
    }

def writer_node(state: GraphState) -> GraphState:
    messages = state['messages']
    response = writer.invoke({"input": messages[-1].content})
    return {
        "messages": messages + [AIMessage(content=response.content)],
        "next": "end"
    }

# Define our edge functions
def router(state: GraphState) -> str:
    return state['next']

def run_langgraph_agents():
    st.header("LangGraph Agents")

    # Define our graph
    workflow = StateGraph(GraphState)

    # Add our nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)

    # Add our edges
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)

    # Set the entry point
    workflow.set_entry_point("researcher")

    # Compile the graph
    app = workflow.compile()

    topic = st.text_input("Enter a topic for the agents to research and summarize:")
    
    if st.button("Run Agents"):
        if topic:
            with st.spinner("Agents are working..."):
                result = app.invoke({
                    "messages": [HumanMessage(content=f"Research and summarize the topic: {topic}")],
                    "next": "researcher"
                })
                st.subheader("Research and Summary:")
                for message in result['messages']:
                    st.write(f"{message.type}: {message.content}")
        else:
            st.warning("Please enter a topic for the agents to work on.")

if __name__ == "__main__":
    run_langgraph_agents()
