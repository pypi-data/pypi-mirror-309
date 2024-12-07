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

from lion.core.typing import ID, Any, JsonValue, override
from lion.libs.parse import to_str

from .message import MessageFlag, MessageRole, RoledMessage
from .utils import format_system_content, validate_sender_recipient


class System(RoledMessage):
    """
    Represents a system message in a language model conversation.

    This class extends RoledMessage to provide functionality specific to
    system messages, which are typically used to set the context or provide
    instructions to the language model. It supports including system datetime
    information and maintains a clean interface for accessing the content.

    Example:
        >>> system_msg = System(
        ...     system="You are a helpful assistant.",
        ...     system_datetime=True
        ... )
        >>> print(system_msg.system_info)
        'System datetime: 2024-01-20T14:30\n\nYou are a helpful assistant.'
    """

    @override
    def __init__(
        self,
        system: JsonValue = None,
        sender: ID.SenderRecipient = None,
        recipient: ID.SenderRecipient = None,
        system_datetime: bool | JsonValue = None,
        protected_init_params: dict | None = None,
    ):
        """
        Initialize a System message instance.

        Args:
            system: The content of the system message
            sender: The sender of the system message
            recipient: The recipient of the message
            system_datetime: Flag to include system datetime
            protected_init_params: Protected initialization parameters

        Raises:
            ValueError: If invalid combination of parameters is provided
        """
        if all(
            x == MessageFlag.MESSAGE_LOAD
            for x in [system, sender, recipient, system_datetime]
        ):
            super().__init__(**protected_init_params)
            return

        if all(
            x == MessageFlag.MESSAGE_CLONE
            for x in [system, sender, recipient, system_datetime]
        ):
            super().__init__(role=MessageRole.SYSTEM)
            return

        super().__init__(
            role=MessageRole.SYSTEM,
            sender=sender or "system",
            content=format_system_content(
                system_datetime=system_datetime, system_message=system
            ),
            recipient=recipient or "N/A",
        )

    def update(
        self,
        system: JsonValue = None,
        sender: ID.SenderRecipient = None,
        recipient: ID.Ref = None,
        system_datetime: bool | str = None,
    ) -> None:
        """
        Update the system message components.

        Args:
            system: New system message content
            sender: New sender
            recipient: New recipient
            system_datetime: New datetime flag or string
        """
        if system:
            self.content = format_system_content(
                system_datetime=system_datetime, system_message=system
            )
        if sender:
            self.sender = validate_sender_recipient(sender)
        if recipient:
            self.recipient = validate_sender_recipient(recipient)

    @property
    def system_info(self) -> str:
        """
        Get the complete system information.

        Returns:
            str: The formatted system information including datetime if present
        """
        if "system_datetime" in self.content:
            msg = f"System datetime: {self.content['system_datetime']}\n\n"
            return msg + f"{self.content['system']}"

        return to_str(self.content["system"])

    @override
    def _format_content(self) -> dict[str, Any]:
        return {"role": self.role.value, "content": self.system_info}
