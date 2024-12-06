from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class RolloutRequest(BaseModel):
    start_urls: list[str]
    tos_level: str = "acceptable"


class RolloutResult(BaseModel):  # TODO: these are the GreedyRollouts, to be deprecated
    output: str
    error: str


class RolloutStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"
    SKIPPED = "skipped"
    QUEUED_FOR_RERUN = "queued_for_rerun"
    READY_FOR_TEST = "ready_for_test"


@dataclass
class Rollout:
    start_url: str
    user_id: str
    status: RolloutStatus
    gcp_storage_path: Optional[str] = None
    phoenix_log_link: Optional[str] = None
    error_message: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    state_updated_at: Optional[datetime] = None
