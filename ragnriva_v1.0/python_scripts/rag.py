"""
rag.py
- User interaction
- load existing data or create a new vector-database from a PDF/Website
- Retrieval Augmented Generation (RAG)
"""

# Imports
import os
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

from dotenv import load_dotenv
import os
load_dotenv()

env_user_agent = os.getenv("USER_AGENT")


# Loads database of existing project or creates new database from PDF/Website
def load_or_create_project():
    # Choose project
    projects = next(os.walk('/mnt/Daten/vector_db'))[1]
    print("Which project do you want to work on?\n-----------------")
    print("\n".join(projects))
    print("new project (type: new)\n-----------------")
    project = input("Choose your project:")

    # Existing project
    if project in projects:
        vector_db = Chroma(
            persist_directory="/mnt/Daten/vector_db/"+project,
            embedding_function=OllamaEmbeddings(model="nomic-embed-text",show_progress=False, base_url="http://localhost:11434"),
            collection_name=project)
    # Project name incorrect
    elif project not in projects and not 'new':
        print('The chosen project does not exist and is not a new project')
        exit()
    # New project
    elif project == 'new':
        # Select project name
        print("Please enter the name of the new project")
        new_project_name = input('project name:')
        # Select datatype (PDF/Website)
        print("------- \nPlease select the type of your input data  \n1: PDF \n2: Website")
        datatype = input("Choose mode (number):")

        # Load and process PDF Document
        if datatype == '1':
            print("Please enter the name of your pdf file")
            pdf_name = input('PDF name:')

            # Split document in chunks
            pages = []
            loader = PyPDFLoader(file_path="/mnt/Daten/"+pdf_name)
            data = loader.load()
            pages.extend(data)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=50)
            text_chunks = []
            for page in pages:
                chunks = text_splitter.split_text(page.page_content)
                text_chunks.extend(chunks)

        # Load and process Website    
        elif datatype == '2':
            print("Please enter the adress of the website")
            url_name = input('URL name:')

            # Split Website in chunks
            loader = WebBaseLoader(url_name)
            data = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=150)
            text_chunks = []
            for document in data:
                chunks = text_splitter.split_text(document.page_content)
                text_chunks.extend(chunks)

        # Create embeddings from text chunks and add the embeddings to the database
        text_documents = [Document(page_content=chunk) for chunk in text_chunks]
        vector_db = Chroma.from_documents(
            documents=text_documents,
            embedding=OllamaEmbeddings(model="nomic-embed-text", show_progress=False, base_url="http://localhost:11434"),
            collection_name=new_project_name,
            persist_directory="/mnt/Daten/vector_db/" + new_project_name)
    return vector_db

# Retrieval chain with prompts to query the database & instruct the llm 
def create_chain(vector_db):
    # LLM
    local_model = "llama3"
    llm = ChatOllama(model=local_model, base_url="http://localhost:11434")

    # Prompt for retrieval
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""")

    # Retriever
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(),
        ChatOllama(model=local_model, base_url="http://localhost:11434"),
        prompt=QUERY_PROMPT
    )

    # Prompt for LLM (added short, precise)
    template = """Answer the question short, precise and based ONLY on the following context:
    {context}
    Question: {question}"""
    prompt = ChatPromptTemplate.from_template(template)

    # Retrieval Chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain