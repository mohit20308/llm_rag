import os
import sys
from typing import Any

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import FakeEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI, \
    HarmCategory, HarmBlockThreshold
from langserve import add_routes
from pydantic import BaseModel

print('Server Starting...')

app = FastAPI(
    title = "RAG System",
    version = "1.0",
    description = "RAG System with PDF Data Source and Sarvam API"
)

def add_api_keys():
    #Loading env file
    load_dotenv('.env')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    SARVAM_API_KEY = os.getenv('SARVAM_API_KEY')

    if GOOGLE_API_KEY == 'None' or GOOGLE_API_KEY == '':
        print('You must specify Google API Key in .env file. Use https://aistudio.google.com/app/apikey to generate key')
        sys.exit(0)

    if SARVAM_API_KEY == 'None' or SARVAM_API_KEY == '':
        print('You must specify Sarvam API Key in .env file. Use https://dashboard.sarvam.ai/ to generate key')
        sys.exit(0)

def load_pdf(file_path):
    pdf_loader = PyPDFLoader(file_path)
    document = pdf_loader.load()
    return document

def split_doc(document):
    #Splitting document into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    splitted_documents = splitter.split_documents(documents = document)
    return splitted_documents

def generate_embeddings(splitted_documents):
    if debug_mode:
        embeddings = FakeEmbeddings(size=4096)
    else:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    return embeddings

def create_vector_store(documents, embeddings):
    vector_store = FAISS.from_documents(documents = documents, embedding = embeddings)
    vector_store.save_local(vector_store_path)
    faiss_retriever = vector_store.as_retriever()
    return faiss_retriever

if __name__ == "__main__":
    add_api_keys()

    debug_mode = False
    file_path = 'iesc111.pdf'
    vector_store_path = 'vectordb'

    document = load_pdf(file_path)
    splitted_documents = split_doc(document)

    embeddings = generate_embeddings(splitted_documents)

    if os.path.exists(vector_store_path + '/index.pkl'):
        print('Loading Vector Store from Local Storage')
        vector_store = FAISS.load_local('vectordb', embeddings=embeddings, allow_dangerous_deserialization=True)
        faiss_retriever = vector_store.as_retriever()
    else:
        faiss_retriever = create_vector_store(splitted_documents, embeddings)

    llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro', safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE})

    #PART 1
    prompt_1 = PromptTemplate.from_template("Answer the following question based solely on the context below: <context> {context} </context> {input}.")
    chain = create_stuff_documents_chain(llm, prompt_1)
    retriver_chain = create_retrieval_chain(faiss_retriever, chain)

    #PART 2
    retriver_tool = create_retriever_tool(
        name='Sound search',
        description='Useful for when you need to search for information about sound. For any questions about sound or sound waves or human hearing, you must use this tool',
        retriever=faiss_retriever
    )

    tools_list_2 = [retriver_tool]
    tools_list_2.extend(load_tools(['llm-math'], llm=llm))

    # Prompt
    prompt_2 = hub.pull("hwchase17/react")
    agent_2 = create_react_agent(llm=llm, tools=tools_list_2, prompt=prompt_2)
    agent_executor_2 = AgentExecutor(agent=agent_2, tools=tools_list_2, verbose=True, handle_parsing_errors=True)  # max_iterations = 30

    #PART 3
    tools_list_3 = [retriver_tool]
    prompt_3 = hub.pull("hwchase17/react")
    agent = create_react_agent(llm = llm, tools = tools_list_3, prompt = prompt_3)
    agent_executor_3 = AgentExecutor(agent=agent, tools=tools_list_3, verbose=True, handle_parsing_errors=True)  # max_iterations = 30

    class Input(BaseModel):
        input: str

    class Output(BaseModel):
        output: Any

    add_routes(app, retriver_chain.with_types(input_type=Input), path = '/part1')
    add_routes(app, agent_executor_2.with_types(input_type=Input, output_type=Output), path = '/part2')
    add_routes(app, agent_executor_3.with_types(input_type=Input, output_type=Output), path = '/part3')

    uvicorn.run(app, host = "localhost", port = 8000)


