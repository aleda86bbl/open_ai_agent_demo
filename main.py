import asyncio

from chat_io_interface import ChatClient, create_restaurant_menu
from pathlib import Path


async def main():
    restaurant_menu = await create_restaurant_menu(menu_path=Path('data/bardo_menu.json'),
                                                   menu_raw_text_file=Path('data/bardo_menu.txt'))
    client = ChatClient(
        restaurant_menu=restaurant_menu,
        voice=True)
    await client.run()


if __name__ == '__main__':
    asyncio.run(main())
