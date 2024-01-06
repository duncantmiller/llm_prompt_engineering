from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class professor"),
    ("user", "{input}")
])

chain = prompt | llm

response = chain.invoke({"input": "hello?"})
print(response.content)
