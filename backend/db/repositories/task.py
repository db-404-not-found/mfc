import uuid
from typing import Any

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import Task
from backend.db.repositories.base import Repository
from backend.utils import clear_text


class TaskRepository(Repository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Task, session=session)

    async def read_by_id(self, task_id: uuid.UUID) -> Task | None:
        return await self._read_by_id(id=task_id)

    async def create(self, question: str) -> Task:
        question = clear_text(question)
        stmt = insert(Task).values(question=question).returning(Task)
        result: ScalarResult[Task] = await self._session.scalars(
            select(Task).from_statement(stmt)
        )
        await self._session.commit()
        task = result.first()
        if task is None:
            raise Exception
        return task

    async def read_task_by_question(self, question: str) -> Task | None:
        question = clear_text(question)
        return (
            await self._session.scalars(select(Task).filter_by(question=question))
        ).first()

    async def update(self, *args: Any, **kwargs: Any) -> Task | None:
        return await self._update(*args, **kwargs)

    async def increment_counter(
        self, task_id: uuid.UUID, cur_value: int
    ) -> Task | None:
        return await self.update(Task.id == task_id, counter=cur_value + 1)
