import asyncio
import json
import queue
from typing import Any, Callable, Mapping, Protocol, Union

import openai.types.chat as openai_chat_types
from betterproto import Casing
from typing_extensions import Literal, runtime_checkable

import maitai_gen.chat as chat_types
from maitai_gen.chat import *
from maitai_gen.chat import (
    ChatCompletionChunk,
    ChatCompletionRequest,
    ChatCompletionResponse,
    Tool,
)


class Omit:
    def __bool__(self) -> Literal[False]:
        return False


Headers = Mapping[str, Union[str, Omit]]
Query = Mapping[str, object]
Body = object


class MaitaiChunk(ChatCompletionChunk):
    def __init__(self, chat_completion_chunk: ChatCompletionChunk = None):
        super().__init__()
        if chat_completion_chunk is not None:
            self.from_pydict(chat_completion_chunk.to_pydict())

    def model_dump_json(self):
        return json.dumps(self.to_pydict(casing=Casing.SNAKE))

    def openai_dump_json(self):
        data = self.to_pydict(casing=Casing.SNAKE)
        # 0 indices and empty arrays get removed by the omit default functions
        if not data.get("choices"):
            data["choices"] = []
        for i, choice in enumerate(data.get("choices")):
            if not choice.get("index"):
                choice["index"] = i
            if choice["delta"].get("tool_calls"):
                for j, tool_call in enumerate(choice["delta"]["tool_calls"]):
                    if not tool_call.get("index"):
                        tool_call["index"] = j
        if data.get("usage"):
            if not data["usage"].get("prompt_tokens"):
                data["usage"]["prompt_tokens"] = 0
            if not data["usage"].get("completion_tokens"):
                data["usage"]["completion_tokens"] = 0
        return openai_chat_types.ChatCompletionChunk(**data).model_dump_json()


class MaitaiCompletion(ChatCompletionResponse):
    def __init__(self, chat_completion_response: ChatCompletionResponse = None):
        super().__init__()
        if chat_completion_response is not None:
            if chat_completion_response.chat_completion_request is not None:
                self.chat_completion_request = ChatCompletionRequest()
            self.from_pydict(chat_completion_response.to_pydict())

    def model_dump_json(self):
        return json.dumps(self.to_pydict(casing=Casing.SNAKE))

    def openai_dump_json(self):
        data = self.to_pydict(casing=Casing.SNAKE)
        # 0 indices and empty arrays get removed by the omit default functions
        for i, choice in enumerate(data.get("choices")):
            if not choice.get("index"):
                choice["index"] = i
            if choice.get("message", {}).get("tool_calls"):
                for j, tool_call in enumerate(choice["message"]["tool_calls"]):
                    if not tool_call.get("index"):
                        tool_call["index"] = j
        return openai_chat_types.ChatCompletion(**data).model_dump_json()


@runtime_checkable
class ToolFunction(Protocol):
    __name__: str
    __doc__: str
    __tool__: Tool

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


ChunkQueue = queue.Queue[
    Union[chat_types.ChatCompletionChunk, StopIteration, Exception]
]
AsyncChunkQueue = asyncio.Queue[
    Union[chat_types.ChatCompletionChunk, StopIteration, Exception]
]


class QueueIterable:
    def __init__(
        self, chunk_queue: Union[ChunkQueue, AsyncChunkQueue], timeout=None
    ) -> None:
        self.queue = chunk_queue
        self.done = False
        self.timeout = timeout

    def __aiter__(self):
        """Returns the asynchronous iterator object itself."""
        return self

    def __iter__(self):
        """Returns the iterator object itself."""
        return self

    def __next__(self) -> chat_types.ChatCompletionChunk:
        while not self.done:
            try:
                # Wait for an item from the queue, block if necessary
                item = self.queue.get(
                    timeout=self.timeout
                )  # Wait for 10 seconds, adjust as needed
                if isinstance(item, StopIteration):
                    self.done = True  # Set done to True to prevent further blocking
                    raise StopIteration
                elif isinstance(item, Exception):
                    raise item
                return item
            except queue.Empty:
                print("Queue timed out")
                self.done = True
                raise TimeoutError
        raise StopIteration

    async def __anext__(self) -> chat_types.ChatCompletionChunk:
        if self.done:
            raise StopAsyncIteration

        try:
            # Wait for an item from the queue with a timeout if specified
            if self.timeout:
                item = await asyncio.wait_for(self.queue.get(), timeout=self.timeout)
            else:
                item = await self.queue.get()

            if isinstance(item, StopIteration):
                self.done = True  # Set done to True to prevent further blocking
                raise StopAsyncIteration
            elif isinstance(item, Exception):
                raise item
            return item

        except asyncio.TimeoutError:
            print("Queue timed out")
            self.done = True
            raise StopAsyncIteration


EvaluateCallback = Callable[[EvaluateResponse], None]
