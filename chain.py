from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

llm = ChatOpenAI()
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a world class professor"),
#     ("user", "{input}")
# ])
output_parser = StrOutputParser()

loader = WebBaseLoader(
    "https://botdevs.ai/articles/prompt-engineering-testing-strategies-with-python"
)
docs = loader.load()
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = DocArrayInMemorySearch.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the context:
                                          <context>
                                          {context}
                                          </context>

                                          Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "what are some best practices for testing prompts?"})
# chain = prompt | llm | output_parser

# response = chain.invoke({"input": "hello?"})
print(response["answer"])


print(vector)
