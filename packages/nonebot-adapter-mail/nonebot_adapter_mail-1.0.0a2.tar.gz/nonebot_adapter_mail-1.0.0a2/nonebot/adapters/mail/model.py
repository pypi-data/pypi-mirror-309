from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from .message import Message


class User(BaseModel):
    id: str
    name: Optional[str] = None


class Mail(BaseModel):
    id: str
    sender: User
    recipients_to: list[User]
    recipients_cc: list[User]
    recipients_bcc: list[User]
    date: Optional[datetime]
    timezone: Optional[float]
    message: "Message"
    original_message: "Message"
    in_reply_to: Optional[str]
