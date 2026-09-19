from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EmailMessage:
    id: str
    sender: str
    subject: str
    snippet: str
    received_at: datetime
