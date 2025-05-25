import asyncio

from chat_io_interface import ChatClient


async def main():
    client = ChatClient(voice=True)
    await client.run()


if __name__ == '__main__':
    asyncio.run(main())
