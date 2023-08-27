from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from backend.api.deps import DatabaseHolderMarker
from backend.api.v1.schemas import QuestionQuerySchema, QuestionResponseSchema
from backend.celery.tasks import make_inference
from backend.db.holder import DatabaseHolder

router = APIRouter(prefix="/v1")


@router.post("/inference", tags=["inference"])
async def create_inference(
    data: QuestionQuerySchema, holder: DatabaseHolder = Depends(DatabaseHolderMarker)
) -> QuestionResponseSchema:
    task = await holder.task.read_task_by_question(question=data.question)
    if task is not None:
        await holder.task.increment_counter(task_id=task.id, cur_value=task.counter)
        return QuestionResponseSchema.model_validate(task)
    task = await holder.task.create(question=data.question)
    make_inference.delay(task_id=task.id)
    return QuestionResponseSchema.model_validate(task)


@router.get("/tasks/{task_id}", tags=["inference"])
async def get_task_by_id(
    task_id: UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)
) -> QuestionResponseSchema:
    task = await holder.task.read_by_id(task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return QuestionResponseSchema.model_validate(task)
