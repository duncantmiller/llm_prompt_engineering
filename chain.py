from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from client import Client

llm = ChatOpenAI(model_name=Client.MODEL_GPT_35)

loader = WebBaseLoader(
    "https://botdevs.ai/articles/prompt-engineering-testing-strategies-with-python"
)
docs = loader.load()
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = DocArrayInMemorySearch.from_documents(documents, embeddings)
retriever = vector.as_retriever()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class professor"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get "
             "information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the following question based only on the context below. If you don't know "
               "the answer say 'I don't know', refrain from guessing or making up an answer. "
               "Here is the context:\n\n<context>{context}</context>"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
chat_history = [HumanMessage(content="what are some best practices for testing prompts?")]
response = retrieval_chain.invoke({
    "chat_history": chat_history,
    "input": "tell me more"
})

print(response["answer"])
