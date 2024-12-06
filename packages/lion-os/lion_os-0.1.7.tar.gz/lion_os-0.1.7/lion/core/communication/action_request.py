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

from typing_extensions import override

from lion.core.typing import ID, Any, Callable, LnID, Note
from lion.libs.parse import to_dict
from lion.libs.utils import copy

from .message import MessageFlag, MessageRole, RoledMessage


def prepare_action_request(
    function: str | Callable,
    arguments: dict,
) -> Note:
    """
    Prepare an action request with function and arguments.

    This function validates and formats the action request parameters,
    ensuring arguments are properly structured as a dictionary.

    Args:
        function: Function to execute, either as name or callable
        arguments: Arguments to pass to the function

    Returns:
        Note: Formatted action request

    Raises:
        ValueError: If arguments cannot be converted to a dictionary
    """
    args = copy(arguments)
    if not isinstance(arguments, dict):
        try:
            arguments = to_dict(args, fuzzy_parse=True, str_type="json", suppress=True)
            if not arguments:
                arguments = to_dict(args, str_type="xml", suppress=True)
            if not arguments or not isinstance(arguments, dict):
                raise ValueError
        except Exception:
            raise ValueError("Arguments must be a dictionary.")
    return Note(action_request={"function": function, "arguments": arguments})


class ActionRequest(RoledMessage):
    """
    Represents a request for an action in the system.

    This class encapsulates the details needed to execute a function call,
    including the function name/reference and its arguments. It also tracks
    whether the request has been responded to.

    Example:
        >>> request = ActionRequest(
        ...     function="calculate_sum",
        ...     arguments={"numbers": [1, 2, 3]},
        ...     sender="user",
        ...     recipient="system"
        ... )
        >>> print(request.function)
        'calculate_sum'
    """

    @override
    def __init__(
        self,
        function: str | Callable | MessageFlag,
        arguments: dict | MessageFlag,
        sender: ID.Ref | MessageFlag = None,
        recipient: ID.Ref | MessageFlag = None,
        protected_init_params: dict | None = None,
    ) -> None:
        """
        Initialize an ActionRequest instance.

        Args:
            function: The function to be invoked
            arguments: The arguments for the function
            sender: The sender of the request
            recipient: The recipient of the request
            protected_init_params: Protected initialization parameters
        """
        message_flags = [function, arguments, sender, recipient]

        if all(x == MessageFlag.MESSAGE_LOAD for x in message_flags):
            protected_init_params = protected_init_params or {}
            super().__init__(**protected_init_params)
            return

        if all(x == MessageFlag.MESSAGE_CLONE for x in message_flags):
            super().__init__(role=MessageRole.ASSISTANT)
            return

        function = function.__name__ if callable(function) else function

        super().__init__(
            role=MessageRole.ASSISTANT,
            content=prepare_action_request(function=function, arguments=arguments),
            sender=sender,
            recipient=recipient,
        )

    @property
    def action_response_id(self) -> LnID | None:
        """
        Get the ID of the corresponding action response.

        Returns:
            LnID | None: The ID of the action response, or None if not responded
        """
        return self.content.get("action_response_id", None)

    @property
    def is_responded(self) -> bool:
        """
        Check if the action request has been responded to.

        Returns:
            bool: True if the request has a response, False otherwise
        """
        return self.action_response_id is not None

    @property
    def request(self) -> dict[str, Any]:
        """
        Get the action request content as a dictionary.

        Returns:
            dict[str, Any]: The request content excluding output
        """
        a = copy(self.content.get("action_request", {}))
        a.pop("output", None)
        return a

    @property
    def arguments(self) -> dict[str, Any]:
        """
        Get the arguments for the action request.

        Returns:
            dict[str, Any]: The arguments dictionary
        """
        return self.request.get("arguments", {})

    @property
    def function(self) -> str:
        """
        Get the function name for the action request.

        Returns:
            str: The name of the function to be invoked
        """
        return self.request.get("function", "")

    @override
    def _format_content(self) -> dict[str, Any]:
        return {"role": self.role.value, "content": self.request}
