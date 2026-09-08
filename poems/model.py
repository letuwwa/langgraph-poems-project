from langchain_ollama import ChatOllama


def create_model() -> ChatOllama:
    return ChatOllama(
        model="gemma2:9b",
        temperature=0.8,
    )
