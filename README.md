# 🏦 Smart Banking FAQ Assistant

An AI-powered Banking FAQ Assistant that uses **Retrieval-Augmented Generation (RAG)** to answer banking-related questions accurately using an official Banking FAQ dataset.

The application performs semantic search over banking documents using vector embeddings and generates context-aware responses through a Local Large Language Model (FLAN-T5).

---

## 🚀 Features

- AI-powered Banking FAQ Assistant
- Semantic Search using Vector Embeddings
- Local Large Language Model (FLAN-T5)
- Retrieval-Augmented Generation (RAG)
- Voice Input Support
- Source Document Display
- Supports Banking FAQs such as:
  - KYC
  - Home Loans
  - Personal Loans
  - Debit/Credit Cards
  - UPI
  - Net Banking
  - Account Opening
  - Fund Transfers

---

# 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- ChromaDB
- Hugging Face Transformers
- Sentence Transformers
- FLAN-T5
- Pandas

---

# 📂 Project Structure

```
Smart-Banking-FAQ-Assistant/
│
├── data/
│   └── banking_faq.csv
│
├── src/
│   ├── loader.py
│   ├── local_llm.py
│   ├── rag.py
│   ├── retriever.py
│   └── vector_store.py
│
├── vector_db/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Samruddhi2103/Smart-Banking-FAQ-Assistant.git
```

### 2. Navigate to Project Folder

```bash
cd Smart-Banking-FAQ-Assistant
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

---

# 🧠 How It Works

1. User enters a banking question through text or voice.
2. The question is converted into embeddings.
3. ChromaDB performs semantic search.
4. The most relevant banking documents are retrieved.
5. FLAN-T5 generates an accurate answer using the retrieved context.
6. The application displays both the answer and the supporting source documents.

---

# 📸 Screenshots

## Home Page

_Add a screenshot here_

## Answer Generation

_Add a screenshot here_

---

# 🔮 Future Enhancements

- User Authentication
- Multilingual Support
- Speech-to-Text & Text-to-Speech
- PDF Banking Policy Search
- Live Banking API Integration
- Chat History Storage
- Mobile Responsive UI

---

# 👩‍💻 Author

**Samruddhi Patil**

MCA Student 

GitHub: https://github.com/Samruddhi2103

---

# ⭐ If you found this project useful, don't forget to Star this repository!