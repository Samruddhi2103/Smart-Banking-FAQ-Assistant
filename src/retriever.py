from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_retriever():

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory="vector_db",
        embedding_function=embedding
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever