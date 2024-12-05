import json
import uuid
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from temporalio.client import Client
from tenacity import retry, stop_after_attempt, wait_exponential

from activities import TranslateParams
from log_config import setup_logging, get_logger
from queue_manager import QueueManager
from settings import settings
from workflow import LangChainWorkflow

logger = get_logger(__name__)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
async def connect_temporal():
    return await Client.connect(f"{settings.TEMPORAL_HOST}:7233")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"connect to temporal: {settings.TEMPORAL_HOST}")
    try:
        app.state.temporal_client = await connect_temporal()
        logger.info("Successfully connected to Temporal")
    except Exception as e:
        logger.error(f"Failed to connect to Temporal after retries: {str(e)}")
        raise
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/translate")
async def translate(phrase: str, language: str):
    client = app.state.temporal_client

    async def event_generator():
        try:
            task_id = str(uuid.uuid4())
            await client.start_workflow(
                LangChainWorkflow.run,
                args=[TranslateParams(phrase, language), task_id],
                id=f"langchain-translation-{task_id}",
                task_queue="langchain-task-queue",
            )

            queue_manager = QueueManager(task_id=task_id)
            async for message in queue_manager.listen():
                yield f"data: {json.dumps(message)}\n\n"

        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    setup_logging()

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )
