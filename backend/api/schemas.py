from typing import Literal

from pydantic import BaseModel


class StatusResponseSchema(BaseModel):
    message: str


class MonitoringSchema(BaseModel):
    status: Literal["ok"]
