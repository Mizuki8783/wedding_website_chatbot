from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_pinecone import PineconeVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.prompts import SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from prompts import agent_system_prompt

embeddings = OpenAIEmbeddings()
vstore = PineconeVectorStore(index_name="wedding-website",embedding=embeddings)
retriever = vstore.as_retriever(search_type="mmr",)

@tool
def retrieve_relevant_info(query):
    """
    Retrieves relevant information to answer the given query.

    Args:
        query (str): The query used to search for relevant information.
    Returns:
        str: A string containing the retrieved information. Each piece of information is formatted as follows:
        - doc_number:<number>
        - blog_title: <title>
        - page_content: <content>
        - summary: <summary>
        - URL: <URL>
    """
    retrieved_docs = retriever.invoke(query)
    retrieved_info = ""
    for i, doc in enumerate(retrieved_docs):
        retrieved_info += f"doc_number:{i+1}\n\nblog_title: {doc.metadata["title"]}. \n\npage_content: {doc.page_content}.\n\n summary: {doc.metadata["summary"]}.\n\n URL: {doc.metadata["sourceURL"]}.\n\n"

    return retrieved_info

def modify_prompt():
    prompt = hub.pull("hwchase17/openai-functions-agent")
    system_message_template = SystemMessagePromptTemplate.from_template(
        agent_system_prompt)
    prompt.messages[0] = system_message_template

    return prompt


def create_agent():
    llm = ChatOpenAI(model="gpt-4o",temperature=0)
    tools = [retrieve_relevant_info]
    prompt = modify_prompt()

    agent_base = create_tool_calling_agent(llm, tools, prompt)
    agent = AgentExecutor(agent=agent_base, tools=tools, verbose=True)

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
