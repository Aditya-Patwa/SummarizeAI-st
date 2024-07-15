from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Loading LLM
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

# Splitting Docs
def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs


# Loading Web Pages
def load_web_page(link):
    loader = WebBaseLoader(link)
    documents = loader.load()
    docs = split_docs(documents)
    chain = load_summarize_chain(llm, chain_type="stuff")
    result = chain.invoke(docs)

    return result["output_text"]
