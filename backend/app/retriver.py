from langchain_community.vectorstores import Chroma
import numpy as np
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

embedding_function = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")

# col_name1 = 'shirt_collection'
# col_name2 = 'pants_collection'

def retriver(col_name, embedding_function, vec_db_path="/Users/Aksorn_AI/Desktop/RECOMENTATION_SYSTEM/backend/vector_db"):
    vectorstore = Chroma(
        collection_name=col_name,
        embedding_function=embedding_function,
        persist_directory=vec_db_path
        )
    retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
            "k": 4,
        }
    )
    return retriever

def search_vector_db(col_name, query):
    id_list = []
    retriever = retriver(col_name, embedding_function, vec_db_path = "/Users/Aksorn_AI/Desktop/RECOMENTATION_SYSTEM/backend/vector_db")
    docs = retriever.get_relevant_documents(query)
    for doc in docs:
        id = doc.metadata['ids']
        id_list.append(id)
    print('id_retrive: ', id_list)
    return id_list
