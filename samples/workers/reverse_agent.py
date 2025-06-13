import asyncio
import logging

from autogen_core import BaseAgent, MessageContext

from autogen_http_runtime.runtimes.http import HttpWorkerAgentRuntime


class ReverseAgent(BaseAgent):
    async def on_message(self, message: str, ctx: MessageContext):
        return message[::-1]


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    rt = HttpWorkerAgentRuntime("http://127.0.0.1:9000")
    await rt.register_factory("reverse", lambda: ReverseAgent())
    await rt.start()
    print("\U0001f527  ReverseAgent registered – waiting for messages…")  # noqa: T201
    await rt.stop_when_signal()


if __name__ == "__main__":
    asyncio.run(main())
