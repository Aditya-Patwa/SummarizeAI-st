from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
import textwrap
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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



def summarize_content(docs):
    # Define prompt
    prompt_template = """
    Write a 5 to 10 paragraph detailed summary of the following:
    "{text}"
    5 TO 10 PARAGRAPH DETAILED SUMMARY:
    """
    prompt = PromptTemplate.from_template(prompt_template)
    # Define LLM chain
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    result = stuff_chain.invoke(docs)

    return result['output_text']

# Loading Web Pages
def load_web_page(link):
    try:
        loader = WebBaseLoader(link)
        documents = loader.load()
        docs = split_docs(documents)
        
        result = summarize_content(docs)
        vectorstore = Chroma.from_documents(documents=docs, embedding=HuggingFaceEmbeddings())
        return (result, vectorstore)
    except:
        return "Unable to load or summarize webpage :sob:"


def load_youtube_video(link):
    loader = YoutubeLoader.from_youtube_url(link,
        add_video_info=True,
        language=["en", "hi"],
        translation="en")
    documents = loader.load()
    docs = split_docs(documents)
    result = summarize_content(docs)
    vectorstore = Chroma.from_documents(documents=docs, embedding=HuggingFaceEmbeddings())
    return (result, vectorstore)



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question(docs, question):
    # Retrieve and generate using the relevant snippets of the blog.
    retriever = docs.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(question)
    return result