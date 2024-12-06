"""
Base mail functionality for the LION communication system.

This module provides the foundational class for mail-like communication,
implementing core functionality for message sending and receiving with
proper ID validation.
"""

from typing import Any

from pydantic import field_validator

from lion.core.generic.element import Element
from lion.core.typing import ID, Communicatable, Field

from .utils import validate_sender_recipient


class BaseMail(Element, Communicatable):
    """
    Base class for mail-like communication in the LION system.

    This class provides the foundation for all message-based communication,
    implementing sender and recipient functionality with proper validation.
    It inherits from Element for core functionality and Communicatable for
    communication capabilities.

    Attributes:
        sender (ID.SenderRecipient): The ID of the sender node or role.
            Can be a specific node ID or one of: "system", "user", "assistant", "N/A"
        recipient (ID.SenderRecipient): The ID of the recipient node or role.
            Can be a specific node ID or one of: "system", "user", "assistant", "N/A"

    Example:
        >>> mail = BaseMail(sender="user", recipient="assistant")
        >>> print(mail.sender)
        'user'
        >>> print(mail.recipient)
        'assistant'
    """

    sender: ID.SenderRecipient = Field(
        default="N/A",
        title="Sender",
        description="The ID of the sender node or a role.",
    )

    recipient: ID.SenderRecipient = Field(
        default="N/A",
        title="Recipient",
        description="The ID of the recipient node or a role.",
    )

    @field_validator("sender", "recipient", mode="before")
    @classmethod
    def _validate_sender_recipient(cls, value: Any) -> ID.SenderRecipient:
        return validate_sender_recipient(value)
