import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessageChunk
from langchain_openai import ChatOpenAI
from temporalio import activity

from log_config import get_logger
from queue_manager import QueueManager
from settings import settings
load_dotenv()
logger = get_logger(__name__)


@dataclass
class TranslateParams:
    phrase: str
    language: str


@activity.defn
async def translate_phrase(params: TranslateParams, task_id: str):
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
    chain = chat_prompt | ChatOpenAI(
        model_name=settings.OPENAI_MODEL,
        openai_api_key=settings.OPENAI_API_KEY,
        openai_api_base=settings.OPENAI_BASE_URL,
    )

    queue_manager = QueueManager(task_id=task_id)

    async for chunk in chain.astream({"phrase": params.phrase, "language": params.language}):
        if isinstance(chunk, AIMessageChunk):
            await queue_manager.publish({
                "status": "success",
                "content": chunk.content
            })
        logger.info(f"published chunk: {chunk}, {type(chunk)}")


@activity.defn
async def complete_phase(task_id: str):
    queue_manager = QueueManager(task_id=task_id)
    await queue_manager.mark_complete()
