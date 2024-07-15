from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

from src.data import constants as const


def retrieve_data(llm_model, vector_db):
    # LLM from Ollama
    # local_model = "mistral"
    llm = ChatOllama(model=llm_model, base_url=f"{const.OLLAMA_HOST}:{const.OLLAMA_PORT}")

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template= const.OLLAMA_INIT_INSTRUCT + """{question}""",
    )

    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), 
        llm,
        prompt=QUERY_PROMPT
    )

    # RAG prompt
    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke("What is this about?")

