import pandas as pd
from langchain_core.documents import Document


def load_csv_data(csv_path):
    """
    Load banking FAQ data from CSV and convert it into LangChain Documents.
    """

    df = pd.read_csv(csv_path)

    documents = []

    for _, row in df.iterrows():

        content = f"""
Question: {row['Question']}

Answer: {row['Answer']}

Category: {row['Category']}
"""

        document = Document(
            page_content=content,
            metadata={
                "category": row["Category"]
            }
        )

        documents.append(document)

    return documents