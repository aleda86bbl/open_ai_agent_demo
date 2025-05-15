from typing import Any

from agents import RunContextWrapper, function_tool
from pydantic_core import to_json

from data_models import MenuItem


@function_tool
def add_food_item(ctx: RunContextWrapper[Any], item: MenuItem) -> str:
    ctx.context.ordered_menu_items.append(item)
    return f'added {item} to menu'


@function_tool
def show_ordered_items(ctx: RunContextWrapper[Any]) -> str:
    ordered_items_string = to_json(ctx.context.ordered_menu_items)
    return f'You have ordered: {ordered_items_string}'
