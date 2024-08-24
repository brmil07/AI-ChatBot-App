from langchain_community.llms import Ollama

llm = Ollama(model="llama3.1")

response = llm.invoke("Tell me a joke!")

print(response)