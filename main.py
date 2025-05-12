import asyncio

from chat_io_interface import TextChatClient
from restaurant_agents import triage_agent


async def main():
    client = TextChatClient(triage_agent)
    await client.run()


if __name__ == '__main__':
    asyncio.run(main())
