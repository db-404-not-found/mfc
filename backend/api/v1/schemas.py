from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.db.models import Status


class QuestionQuerySchema(BaseModel):
    question: str


class QuestionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: Status
    result: str | None = None
