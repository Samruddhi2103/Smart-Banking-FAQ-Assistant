from src.retriever import get_retriever
from src.local_llm import generate_answer


def ask_question(question):

    retriever = get_retriever()

    documents = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in documents])

    answer = generate_answer(context, question)

    return answer, documents