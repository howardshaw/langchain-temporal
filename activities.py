# activities.py
from dataclasses import dataclass

from temporalio import activity

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


@dataclass
class TranslateParams:
    phrase: str
    language: str


@activity.defn
async def translate_phrase(params: TranslateParams) -> dict:
    # LangChain setup
    template = """You are a helpful assistant who translates between languages.
    Translate the following phrase into the specified language: {phrase}
    Language: {language}"""
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", "Translate"),
        ]
    )
    chain = chat_prompt | ChatOpenAI()

    return chain.invoke({"phrase": params.phrase, "language": params.language})
