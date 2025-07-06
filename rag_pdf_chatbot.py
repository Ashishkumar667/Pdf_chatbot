import os
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI


load_dotenv()

def load_pdf_and_create_vectorstore(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    print(f"[DEBUG] Vectorstore created with {len(chunks)} chunks.")
    for i, chunk in enumerate(chunks):
        print(f"[Chunk {i+1}]: {chunk.page_content[:100]}...")

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

    return vectorstore

# def get_qa_chain(vectorstore):
#     retriever = vectorstore.as_retriever()
#     llm = OpenAI(temperature=0)
#     chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=retriever,
#         return_source_documents=True
#     )
#     return chain
def get_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    llm = OpenAI(temperature=0)
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return chain
