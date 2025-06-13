# Autogen HTTP Runtime

Autogen HTTP Runtime provides an HTTP based implementation of the
`AgentRuntime` protocol from [autogen-core](https://github.com/microsoft/autogen).
It uses FastAPI and WebSockets to let agent workers communicate with a
central host over JSON-RPC.

## Installation

```bash
pip install autogen-http-runtime
```

## Quick start

The example below mirrors the behaviour tested under `tests/test_http_runtime.py`.
It sets up a host, registers an agent factory and then sends a message between
agents over HTTP:

```python
import asyncio
from pydantic import BaseModel
from autogen_http_runtime.runtimes.http import HttpWorkerAgentRuntime, HttpAgentServer
from autogen_core import MessageContext, rpc, RoutedAgent
from autogen_core._serialization import PydanticJsonMessageSerializer

class Ping(BaseModel):
    content: str = "ping"

class Pong(BaseModel):
    content: str

class CalleeAgent(RoutedAgent):
    @rpc
    async def on_ping(self, message: Ping, ctx: MessageContext) -> Pong:
        return Pong(content=f"pong: {message.content}")

async def main() -> None:
    host = HttpAgentServer(port=8000)
    host.start()

    callee_rt = HttpWorkerAgentRuntime("http://127.0.0.1:8000")
    await callee_rt.register_factory("callee", CalleeAgent)
    callee_rt.add_message_serializer([
        PydanticJsonMessageSerializer(Ping),
        PydanticJsonMessageSerializer(Pong),
    ])
    await callee_rt.start()

    caller_rt = HttpWorkerAgentRuntime("http://127.0.0.1:8000")
    caller_rt.add_message_serializer([
        PydanticJsonMessageSerializer(Ping),
        PydanticJsonMessageSerializer(Pong),
    ])
    await caller_rt.start()

    callee_id = await caller_rt.get("callee")
    result: Pong = await caller_rt.send_message(Ping(content="hello"), recipient=callee_id)
    print(result)

    await caller_rt.stop()
    await callee_rt.stop()
    await host.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Running the tests

The project uses `pytest` for testing. After installing the development
dependencies, run:

```bash
pytest
```

## License

This project is licensed under the MIT License.
