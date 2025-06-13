import asyncio
import logging

from autogen_core import AgentId

from autogen_http_runtime.runtimes.http import HttpWorkerAgentRuntime


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    rt = HttpWorkerAgentRuntime("http://127.0.0.1:9000")
    await rt.start()

    reverse = AgentId("reverse", "default")
    upper = AgentId("upper", "default")

    txt = "Hello distributed HTTP runtime!"
    out1 = await rt.send_message(txt, reverse)
    out2 = await rt.send_message(txt, upper)
    print(f"{reverse.type} → {out1}")  # noqa: T201
    print(f"{upper.type}   → {out2}")  # noqa: T201

    await rt.stop()


if __name__ == "__main__":
    asyncio.run(main())
