import json
from datetime import datetime, timezone
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, field_serializer, field_validator

# Letta API style responses (intended to be easier to use vs getting true Message types)


class LettaMessage(BaseModel):
    """
    Base class for simplified Letta message response type. This is intended to be used for developers who want the internal monologue, function calls, and function returns in a simplified format that does not include additional information other than the content and timestamp.

    Attributes:
        id (str): The ID of the message
        date (datetime): The date the message was created in ISO format

    """

    # NOTE: use Pydantic's discriminated unions feature: https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions
    # see `message_type` attribute

    id: str
    date: datetime

    @field_serializer("date")
    def serialize_datetime(self, dt: datetime, _info):
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            dt = dt.replace(tzinfo=timezone.utc)
        # Remove microseconds since it seems like we're inconsistent with getting them
        # TODO figure out why we don't always get microseconds (get_utc_time() does)
        return dt.isoformat(timespec="seconds")


class SystemMessage(LettaMessage):
    """
    A message generated by the system. Never streamed back on a response, only used for cursor pagination.

    Attributes:
        message (str): The message sent by the system
        id (str): The ID of the message
        date (datetime): The date the message was created in ISO format
    """

    message_type: Literal["system_message"] = "system_message"
    message: str


class UserMessage(LettaMessage):
    """
    A message sent by the user. Never streamed back on a response, only used for cursor pagination.

    Attributes:
        message (str): The message sent by the user
        id (str): The ID of the message
        date (datetime): The date the message was created in ISO format
    """

    message_type: Literal["user_message"] = "user_message"
    message: str


class InternalMonologue(LettaMessage):
    """
    Representation of an agent's internal monologue.

    Attributes:
        internal_monologue (str): The internal monologue of the agent
        id (str): The ID of the message
        date (datetime): The date the message was created in ISO format
    """

    message_type: Literal["internal_monologue"] = "internal_monologue"
    internal_monologue: str


class FunctionCall(BaseModel):

    name: str
    arguments: str
    function_call_id: str


class FunctionCallDelta(BaseModel):

    name: Optional[str]
    arguments: Optional[str]
    function_call_id: Optional[str]

    # NOTE: this is a workaround to exclude None values from the JSON dump,
    # since the OpenAI style of returning chunks doesn't include keys with null values
    def model_dump(self, *args, **kwargs):
        kwargs["exclude_none"] = True
        return super().model_dump(*args, **kwargs)

    def json(self, *args, **kwargs):
        return json.dumps(self.model_dump(exclude_none=True), *args, **kwargs)


class FunctionCallMessage(LettaMessage):
    """
    A message representing a request to call a function (generated by the LLM to trigger function execution).

    Attributes:
        function_call (Union[FunctionCall, FunctionCallDelta]): The function call
        id (str): The ID of the message
        date (datetime): The date the message was created in ISO format
    """

    message_type: Literal["function_call"] = "function_call"
    function_call: Union[FunctionCall, FunctionCallDelta]

    # NOTE: this is required for the FunctionCallDelta exclude_none to work correctly
    def model_dump(self, *args, **kwargs):
        kwargs["exclude_none"] = True
        data = super().model_dump(*args, **kwargs)
        if isinstance(data["function_call"], dict):
            data["function_call"] = {k: v for k, v in data["function_call"].items() if v is not None}
        return data

    class Config:
        json_encoders = {
            FunctionCallDelta: lambda v: v.model_dump(exclude_none=True),
            FunctionCall: lambda v: v.model_dump(exclude_none=True),
        }

    # NOTE: this is required to cast dicts into FunctionCallMessage objects
    # Without this extra validator, Pydantic will throw an error if 'name' or 'arguments' are None
    # (instead of properly casting to FunctionCallDelta instead of FunctionCall)
    @field_validator("function_call", mode="before")
    @classmethod
    def validate_function_call(cls, v):
        if isinstance(v, dict):
            if "name" in v and "arguments" in v and "function_call_id" in v:
                return FunctionCall(name=v["name"], arguments=v["arguments"], function_call_id=v["function_call_id"])
            elif "name" in v or "arguments" in v or "function_call_id" in v:
                return FunctionCallDelta(name=v.get("name"), arguments=v.get("arguments"), function_call_id=v.get("function_call_id"))
            else:
                raise ValueError("function_call must contain either 'name' or 'arguments'")
        return v


class FunctionReturn(LettaMessage):
    """
    A message representing the return value of a function call (generated by Letta executing the requested function).

    Attributes:
        function_return (str): The return value of the function
        status (Literal["success", "error"]): The status of the function call
        id (str): The ID of the message
        date (datetime): The date the message was created in ISO format
        function_call_id (str): A unique identifier for the function call that generated this message
    """

    message_type: Literal["function_return"] = "function_return"
    function_return: str
    status: Literal["success", "error"]
    function_call_id: str


# Legacy Letta API had an additional type "assistant_message" and the "function_call" was a formatted string


class AssistantMessage(LettaMessage):
    message_type: Literal["assistant_message"] = "assistant_message"
    assistant_message: str


class LegacyFunctionCallMessage(LettaMessage):
    function_call: str


LegacyLettaMessage = Union[InternalMonologue, AssistantMessage, LegacyFunctionCallMessage, FunctionReturn]


LettaMessageUnion = Annotated[
    Union[SystemMessage, UserMessage, InternalMonologue, FunctionCallMessage, FunctionReturn, AssistantMessage],
    Field(discriminator="message_type"),
]
