from typing import Any, Dict

from agents import RunContextWrapper, function_tool
from pydantic_core import to_json

from data_models import MenuItem, OrderState


@function_tool
def add_food_item(ctx: RunContextWrapper[Any], item: MenuItem) -> str:
    ctx.context.ordered_menu_items.append(item)
    ctx.context.order_state = OrderState.READY_TO_ORDER
    return f'added {item} to menu'


@function_tool
def remove_food_item(ctx: RunContextWrapper[Any], item: MenuItem) -> str:
    ctx.context.ordered_menu_items.remove(item)
    ctx.context.order_state = OrderState.READY_TO_ORDER
    return f'removed {item} from menu'


@function_tool
def show_ordered_items(ctx: RunContextWrapper[Any]) -> str:
    ordered_items_string = to_json(ctx.context.ordered_menu_items)
    return f'You have ordered: {ordered_items_string}'


@function_tool
def finish_order(ctx: RunContextWrapper[Any]) -> str:
    ctx.context.order_state = OrderState.DONE_WITH_ORDER
    return f'Your order is complete.'


@function_tool
def calculate_bill_for_order(ctx: RunContextWrapper[Any]) -> Dict[str, str]:
    ctx.context.order_state = OrderState.READY_TO_PAY
    total = 0
    for ordered_item in ctx.context.ordered_menu_items:
        total += ordered_item.price

    vat_charge = total * 0.07
    service_charge = total * 0.1
    to_pay = total + vat_charge + service_charge

    bill = {'total': total,
            'VAT': vat_charge,
            'service_charge': service_charge,
            'to_pay': to_pay}
    return bill
