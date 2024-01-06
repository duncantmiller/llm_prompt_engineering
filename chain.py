from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class professor"),
    ("user", "{input}")
])
output_parser = StrOutputParser()

loader = WebBaseLoader("https://botdevs.ai/articles/prompt-engineering-testing-strategies-with-python")
docs = loader.load()
embeddings = OpenAIEmbeddings()

# chain = prompt | llm | output_parser

# response = chain.invoke({"input": "hello?"})
# print(response)

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = DocArrayInMemorySearch.from_documents(documents, embeddings)
print(vector)
