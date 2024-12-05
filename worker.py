import asyncio

from temporalio.worker import Worker

from activities import translate_phrase, complete_phase
from log_config import setup_logging, get_logger
from server import connect_temporal
from workflow import LangChainWorkflow

interrupt_event = asyncio.Event()

logger = get_logger(__name__)


async def main():
    client = await connect_temporal()
    worker = Worker(
        client,
        task_queue="langchain-task-queue",
        workflows=[LangChainWorkflow],
        activities=[translate_phrase, complete_phase],
    )

    logger.info("Worker started, ctrl+c to exit")
    await worker.run()
    try:
        # Wait indefinitely until the interrupt event is set
        await interrupt_event.wait()
    finally:
        # The worker will be shutdown gracefully due to the async context manager
        logger.info("Shutting down the worker")


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
