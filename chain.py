from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

llm = ChatOpenAI()

output_parser = StrOutputParser()

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
    ("system", "Answer the following question based only on the context:"
               "\n\n<context>{context}</context>"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
chat_history = []
response = retrieval_chain.invoke({
    "chat_history": chat_history,
    "input": "what are some best practices for testing prompts?"
})
# chain = prompt | llm | output_parser

# response = chain.invoke({"input": "hello?"})
print(response["answer"])


print(vector)
