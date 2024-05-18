from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_pinecone import PineconeVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.prompts import SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage


from prompts import agent_system_prompt

def connect_to_retriever():
    embeddings = OpenAIEmbeddings()
    vstore = PineconeVectorStore(index_name="wedding-website",embedding=embeddings)
    retriever = vstore.as_retriever()

    return retriever

def turn_retriever_into_tool():
    retriever = connect_to_retriever()
    retriever_tool= create_retriever_tool(
        retriever,
        "wedding_ideas_and_trend_search",
        "Search for information about wedding related ideas and trend. For any questions related to wedding and wedding planning, you MUST use this tool!"
        )

    return retriever_tool

def modify_prompt():
    prompt = hub.pull("hwchase17/openai-functions-agent")
    system_message_template = SystemMessagePromptTemplate.from_template(
        agent_system_prompt)
    prompt.messages[0] = system_message_template

    return prompt


def create_agent():
    llm = ChatOpenAI(model="gpt-4o",temperature=0)
    retriever_tool = turn_retriever_into_tool()
    tools = [retriever_tool]
    prompt = modify_prompt()

    agent_base = create_tool_calling_agent(llm, tools, prompt)
    agent = AgentExecutor(agent=agent_base, tools=tools)

    return agent

def clean_history(chat_history):
    history = []
    print(chat_history)
    for message in chat_history.split("_end_of_message_"):
        speaker, content = message.split(": ", 1)
        if speaker == "AI_MESSAGE":
            history.append(AIMessage(content))
        else:
            history.append(HumanMessage(content))

    return history

def get_response(agent_executor, query, chat_history):
    clean_chat_history = clean_history(chat_history)
    response = agent_executor.invoke({
        "chat_history": clean_chat_history,
        "input": query,
    })

    return response["output"]
