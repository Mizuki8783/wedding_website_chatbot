from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_pinecone import PineconeVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.prompts import SystemMessagePromptTemplate

from prompts import agent_system_prompt

def connect_to_retriever():
    embeddings = OpenAIEmbeddings()
    vstore = PineconeVectorStore(index_name="chatagent",embedding=embeddings)
    retriever = vstore.as_retriever()

    return retriever

def turn_retriever_into_tool():
    retriever = connect_to_retriever()
    retriever_tool= create_retriever_tool(
        retriever,
        "cold_exposure_search",
        "Search for information about cold exposure. For any questions about cold exposure, you must use this tool!"
        )

    return retriever_tool

def modify_prompt():
    prompt = hub.pull("hwchase17/openai-functions-agent")
    system_message_template = SystemMessagePromptTemplate.from_template(agent_system_prompt)
    prompt.messages[0] = system_message_template

    return prompt

def create_agent():
    llm = ChatOpenAI(temperature=0)
    retriever_tool = turn_retriever_into_tool()
    tools = [retriever_tool]
    prompt = modify_prompt()

    agent_base = create_tool_calling_agent(llm, tools, prompt)
    agent = AgentExecutor(agent=agent_base, tools=tools)

    return agent

def get_response(agent_executor,query,chat_history):
    response =  agent_executor.invoke({
        "chat_history": chat_history,
        "input": query,
    })

    return response["output"]
