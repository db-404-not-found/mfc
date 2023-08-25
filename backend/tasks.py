from uuid import UUID

from celery import Celery
from loguru import logger

from backend.config import Settings

settings = Settings()

celery = Celery("worker", broker=settings.build_celery_broker_url(), backend="rpc://")


@celery.task(name="inference_task")
def make_inference(task_id: UUID) -> None:
    logger.info("Task with ID {task_id} got !!!!!!!", task_id=task_id)
