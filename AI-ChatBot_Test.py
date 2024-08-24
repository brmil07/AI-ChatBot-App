from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def init_model():
    template = """
    Answer the question below.
    Here is the conversation history: {context}
    Question: {question}
    Answer:
    """

    model = OllamaLLM(model="llama3.1")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain


def handle_conversation(chain):
    context = ""
    print("Welcome to the AI ChatBot App!\nType 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"


def main():
    chain = init_model()
    handle_conversation(chain)


if __name__ == "__main__":
    main()
