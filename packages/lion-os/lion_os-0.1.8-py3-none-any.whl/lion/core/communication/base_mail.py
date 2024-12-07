"""
Copyright 2024 HaiyangLi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from lion.core.generic import Element
from lion.core.typing import ID, Any, Communicatable, Field, field_validator

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
