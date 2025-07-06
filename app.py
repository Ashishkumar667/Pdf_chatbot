import streamlit as st
from rag_pdf_chatbot import load_pdf_and_create_vectorstore, get_qa_chain

st.set_page_config(page_title="📚 PDF Chatbot")
st.title("🤖 Chat with your PDF using RAG")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processing PDF..."):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        vectorstore = load_pdf_and_create_vectorstore("temp.pdf")
        qa_chain = get_qa_chain(vectorstore)

    st.success("✅ PDF processed! Ask your question below.")

    question = st.text_input("❓ Ask a question about the PDF")

    if st.button("Get Answer") and question:
        response = qa_chain.invoke({"query": question})

        st.markdown(f"**Answer:** {response['result']}")

        with st.expander("📄 Retrieved Chunks"):
            for i, doc in enumerate(response["source_documents"]):
                st.markdown(f"**Chunk {i+1}:** {doc.page_content[:300]}...")
