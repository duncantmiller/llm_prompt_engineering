from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI()

response = llm.invoke("hello?")

print(response.content)
