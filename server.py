# server.py
import uvicorn
from fastapi import FastAPI, HTTPException
from temporalio.client import Client

from activities import TranslateParams
from workflow import LangChainWorkflow

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.temporal_client = await Client.connect("localhost:7233")


@app.post("/translate")
async def translate(phrase: str, language: str):
    client = app.state.temporal_client
    try:
        result = await client.execute_workflow(
            LangChainWorkflow.run,
            TranslateParams(phrase, language),
            id=f"langchain-translation-{language}-{phrase}",
            task_queue="langchain-task-queue",
        )
        translation_content = result.get("content", "Translation not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"translation": translation_content}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
