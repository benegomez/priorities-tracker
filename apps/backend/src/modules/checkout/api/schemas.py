from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CheckOutCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    checkin_id: UUID


class MarkCompletedRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    completed: bool


class CheckOutSubmitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    notes: str | None = None
    lessons_learned: str | None = None


class CheckOutPriorityItem(BaseModel):
    id: UUID
    title: str
    status: str
    priority_level: str
    completed: bool
    tasks: list["CheckOutTaskItem"] = []


class CheckOutTaskItem(BaseModel):
    id: UUID
    title: str
    status: str
    completed: bool


class CheckOutResponse(BaseModel):
    id: UUID
    checkin_id: UUID
    employee_id: UUID
    organization_id: UUID
    week_start: date
    status: str
    submitted_at: datetime | None = None
    notes: str | None = None
    lessons_learned: str | None = None
    priorities: list[CheckOutPriorityItem] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MarkPriorityResponse(BaseModel):
    priority_id: UUID
    completed: bool


class MarkTaskResponse(BaseModel):
    task_id: UUID
    completed: bool


class CheckOutSummaryResponse(BaseModel):
    priorities_total: int
    priorities_completed: int
    priorities_carried: int
    tasks_total: int
    tasks_completed: int


class CheckOutSubmitResponse(BaseModel):
    id: UUID
    status: str
    submitted_at: datetime | None = None
    summary: CheckOutSummaryResponse
