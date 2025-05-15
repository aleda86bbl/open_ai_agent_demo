import asyncio

from chat_io_interface import TextChatClient


async def main():
    client = TextChatClient()
    await client.run()


if __name__ == '__main__':
    asyncio.run(main())
