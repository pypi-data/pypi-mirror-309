# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.27.0
# Pydantic Version: 2.8.2
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class Model(BaseModel):
    id: int = Field(default=0)
    date_added: int = Field(default=0)
    company_id: int = Field(default=0)
    provider: str = Field(default="")
    model: str = Field(default="")
    points_to: typing.Optional[str] = Field(default="")
    status: str = Field(default="")
    use_fallback: bool = Field(default=False)
    rate_limited: bool = Field(default=False)
    base_url: typing.Optional[str] = Field(default="")
    token: typing.Optional[str] = Field(default="")
    model_ref: str = Field(default="")
    hosted_name: typing.Optional[str] = Field(default="")
