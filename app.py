import streamlit as st
from extractor import extract_all
from analyst import ask_question, summarise_document

# --- Page config ---
st.set_page_config(
    page_title="Document Analyst",
    page_icon="📄",
    layout="wide"
)

# --- Header ---
st.title("📄 Document Analyst")
st.caption("Upload any PDF and chat with it using GPT-4o")

# --- Session state setup ---
if "extracted" not in st.session_state:
    st.session_state.extracted = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "summary" not in st.session_state:
    st.session_state.summary = None
if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = None

# --- Sidebar: file upload ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

    if uploaded_file:
        # Only extract if this is a NEW file
        if uploaded_file.name != st.session_state.last_uploaded:
            pdf_bytes = uploaded_file.read()
            with st.spinner("Extracting content..."):
                st.session_state.extracted = extract_all(pdf_bytes)
                st.session_state.chat_history = []
                st.session_state.summary = None
                st.session_state.last_uploaded = uploaded_file.name

        stats = st.session_state.extracted["stats"]
        st.success("Document loaded!")
        st.metric("Characters", f"{stats['text_length']:,}")
        st.metric("Tables", stats["table_count"])
        st.metric("Images", stats["image_count"])

    st.divider()
    if st.button("Clear chat history"):
        st.session_state.chat_history = []
        st.rerun()

# --- Main area ---
if st.session_state.extracted is None:
    st.info("Upload a PDF in the sidebar to get started.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**What you can do**")
        st.markdown("- Summarise any document")
        st.markdown("- Ask questions in plain English")
        st.markdown("- Extract data from tables")
    with col2:
        st.markdown("**Works great for**")
        st.markdown("- Financial reports")
        st.markdown("- Legal contracts")
        st.markdown("- Research papers")
    with col3:
        st.markdown("**Powered by**")
        st.markdown("- GPT-4o")
        st.markdown("- PyMuPDF")
        st.markdown("- pdfplumber")

else:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Document Summary")
        if st.session_state.summary is None:
            with st.spinner("Generating summary..."):
                st.session_state.summary = summarise_document(
                    st.session_state.extracted
                )
        st.write(st.session_state.summary)

        with st.expander("View extracted text"):
            st.text(st.session_state.extracted["text"][:3000])
            if len(st.session_state.extracted["text"]) > 3000:
                st.caption("Showing first 3000 characters...")

        if st.session_state.extracted["tables"]:
            with st.expander("View extracted tables"):
                for i, table in enumerate(st.session_state.extracted["tables"]):
                    st.caption(f"Table {i+1} — Page {table['page']}")
                    st.dataframe(table["data"])

    with col2:
        st.subheader("Chat with your document")

        # Display full chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Chat input
        question = st.chat_input("Ask anything about the document...")

        if question:
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_question(
                        question,
                        st.session_state.extracted,
                        st.session_state.chat_history
                    )
                st.write(answer)

            # Save ONCE to history
            st.session_state.chat_history.append(
                {"role": "user", "content": question}
            )
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )