import streamlit as st
from streamlit_mic_recorder import speech_to_text
from src.rag import ask_question

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Smart Banking FAQ Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — bank-style theme (navy + gold)
# ============================================================
st.markdown("""
<style>
    /* Force light theme regardless of browser/OS dark mode */
    :root, .stApp {
        color-scheme: light !important;
        --text-color: #1a2333 !important;
        --background-color: #f4f6f9 !important;
        --secondary-background-color: #ffffff !important;
    }

    /* Overall app background */
    .stApp {
        background-color: #f4f6f9;
    }

    /* Hide default streamlit chrome */
    #MainMenu, footer {visibility: hidden;}

    /* ---- Force readable dark text everywhere in the main content ---- */
    .main, .block-container {
        color: #1a2333 !important;
    }
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {
        color: #1a2333 !important;
    }
    .block-container [data-testid="stMarkdownContainer"] h4 {
        color: #0b1f3a !important;
        font-weight: 700 !important;
    }

    /* Bank header banner keeps its own white text.
       Selector is written to out-specify the generic dark-text rule above. */
    [data-testid="stMarkdownContainer"] .bank-header,
    [data-testid="stMarkdownContainer"] .bank-header h1,
    [data-testid="stMarkdownContainer"] .bank-header p,
    [data-testid="stMarkdownContainer"] .bank-header span {
        color: #ffffff !important;
    }
    [data-testid="stMarkdownContainer"] .bank-header p {
        color: #c9d6e8 !important;
    }

    /* Text input value + label */
    .stTextInput label, .stTextInput p {
        color: #1a2333 !important;
    }
    .stTextInput input {
        color: #1a2333 !important;
        background-color: #ffffff !important;
    }
    .stTextInput input::placeholder {
        color: #8a94a3 !important;
        opacity: 1 !important;
    }

    /* Top banner */
    .bank-header {
        background: linear-gradient(90deg, #0b1f3a 0%, #13315c 100%);
        padding: 28px 36px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(11, 31, 58, 0.25);
    }
    .bank-header h1 {
        color: #ffffff;
        font-size: 30px;
        margin: 0;
        font-weight: 700;
    }
    .bank-header p {
        color: #c9d6e8;
        margin: 4px 0 0 0;
        font-size: 15px;
    }

    /* Section card */
    .card {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px 28px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e7ebf1;
        margin-bottom: 20px;
    }

    .card h4 {
        color: #0b1f3a;
        margin-top: 0;
        font-size: 16px;
        font-weight: 600;
    }

    /* Divider label "OR" */
    .or-divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #9aa5b1;
        font-weight: 600;
        font-size: 13px;
        margin: 6px 0 18px 0;
    }
    .or-divider::before, .or-divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e0e4ea;
    }
    .or-divider::before { margin-right: 12px; }
    .or-divider::after { margin-left: 12px; }

    /* Current question chip */
    .question-box {
        background: #eef4ff;
        border-left: 4px solid #13315c;
        padding: 14px 18px;
        border-radius: 8px;
        color: #0b1f3a;
        font-size: 15px;
        min-height: 24px;
    }

    /* Answer box */
    .answer-box {
        background: #f4faf6;
        border-left: 4px solid #1f9d55;
        padding: 18px 20px;
        border-radius: 8px;
        color: #14351f;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Ask button */
    div.stButton > button {
        background-color: #c9a227;
        color: #0b1f3a;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 26px;
        font-size: 15px;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background-color: #b8911f;
        color: #ffffff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b1f3a;
    }
    section[data-testid="stSidebar"] * {
        color: #e6ecf5 !important;
    }

    /* Text input */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #d5dbe4;
        padding: 10px 12px;
    }

    /* Expander (source docs) */
    .streamlit-expanderHeader, [data-testid="stExpander"] summary {
        background-color: #f4f6f9 !important;
        border-radius: 6px;
        font-weight: 600 !important;
        color: #0b1f3a !important;
    }
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
        color: #1a2333 !important;
    }
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e7ebf1 !important;
    }

    /* Footer disclaimer */
    .disclaimer {
        text-align: center;
        color: #9aa5b1;
        font-size: 12px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = None
if "docs" not in st.session_state:
    st.session_state.docs = None

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🏦 SecureBank Assist")
    st.markdown("---")
    st.markdown("**About**")
    st.write("Ask questions about accounts, cards, loans, KYC, transfers, and more — powered by AI over our official FAQ documents.")
    st.markdown("---")
    st.markdown("**Popular Topics**")
    for topic in ["Account Opening", "Debit/Credit Cards", "Fund Transfers (NEFT/RTGS/UPI)",
                "Loan Eligibility", "KYC Requirements", "Net Banking Login Issues"]:
        st.markdown(f"- {topic}")
    st.markdown("---")
    st.caption("For account-specific issues, please contact your branch or call 1800-XXX-XXXX.")

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="bank-header">
    <h1>🏦 Smart Banking FAQ Assistant</h1>
    <p>Get instant, accurate answers to your banking questions — by typing or speaking.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# INPUT SECTION
# ============================================================
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ⌨️ Type your question")
    text_input = st.text_input(
        "Enter your banking question",
        value=st.session_state.question,
        placeholder="e.g. How do I reset my net banking password?",
        label_visibility="collapsed"
    )
    if text_input:
        st.session_state.question = text_input
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🎤 Or ask by voice")
    voice_text = speech_to_text(
        language="en",
        use_container_width=True,
        just_once=True,
        key="voice"
    )
    if voice_text:
        st.session_state.question = voice_text
        st.success("Voice captured successfully")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# CURRENT QUESTION
# ============================================================
st.markdown("#### 📝 Current Question")
st.markdown(
    f'<div class="question-box">{st.session_state.question if st.session_state.question else "No question entered yet."}</div>',
    unsafe_allow_html=True
)

st.write("")

# ============================================================
# ASK BUTTON
# ============================================================
ask_col, _ = st.columns([1, 4])
with ask_col:
    ask_clicked = st.button("🔍 Get Answer", use_container_width=True)

if ask_clicked:
    if st.session_state.question.strip() == "":
        st.warning("Please enter or speak a question first.")
    else:
        with st.spinner("Searching official banking FAQs..."):
            answer, docs = ask_question(st.session_state.question)
            st.session_state.answer = answer
            st.session_state.docs = docs

# ============================================================
# RESULTS
# ============================================================
if st.session_state.answer:
    st.divider()
    st.markdown("### 💡 Answer")
    st.markdown(f'<div class="answer-box">{st.session_state.answer}</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### 📄 Source Documents")

    if st.session_state.docs:
        for i, doc in enumerate(st.session_state.docs, start=1):
            with st.expander(f"📎 Document {i}"):
                st.write(doc.page_content)
    else:
        st.caption("No source documents returned.")

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    '<div class="disclaimer">This assistant provides general information only and is not a substitute for official bank communication.</div>',
    unsafe_allow_html=True
)
