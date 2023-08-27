import uuid
from enum import StrEnum

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ChoiceType

from backend.db.base import Base


class Status(StrEnum):
    QUEUED = "QUEUED"
    STARTED = "STARTED"
    RESPONSED = "RESPONSED"


class Task(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    status: Mapped[Status] = mapped_column(
        ChoiceType(Status, impl=String(32)),
        nullable=False,
        default=Status.QUEUED,
    )
    question: Mapped[str] = mapped_column(String(2048), nullable=False)
    result: Mapped[str] = mapped_column(String, nullable=True, default=None)
    counter: Mapped[int] = mapped_column(Integer, nullable=True, default=1)

    def __repr__(self) -> str:
        return f"Task({self.id}, {self.status})"
