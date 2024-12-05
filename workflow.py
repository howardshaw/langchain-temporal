from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import TranslateParams, translate_phrase, complete_phase

from log_config import get_logger

logger = get_logger(__name__)


@workflow.defn
class LangChainWorkflow:

    @workflow.run
    async def run(self, params: TranslateParams, task_id: str) -> None:
        logger.info(f"workflow run_id: {workflow.info().run_id}, task_id: {task_id}")
        await workflow.execute_activity(
            translate_phrase,
            args=[params, task_id],
            schedule_to_close_timeout=timedelta(seconds=30),
        )
        logger.info("activity translate_phrase done")
        await workflow.execute_activity(
            complete_phase,
            task_id,
            schedule_to_close_timeout=timedelta(seconds=30),
        )

        logger.info("workflow done")
