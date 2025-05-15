from pydantic import BaseModel
from enum import StrEnum


class MenuItem(BaseModel):
    item_number: int
    name: str
    description: str
    price: float
    recommended: bool
    vegetarian: bool


class MenuSection(BaseModel):
    name: str
    menu_items: list[MenuItem]


class RestaurantMenu(BaseModel):
    menu_sections: list[MenuSection]
    currency: str
    prices_include_service_charge: bool


class OrderState(StrEnum):
    READY_TO_ORDER = 'ready_to_order'
    DONE_WITH_ORDER = 'done_with_order'
    READY_TO_PAY = 'ready_to_pay'


class RestaurantOrder(BaseModel):
    ordered_menu_items: list[MenuItem] = []
    order_state: OrderState = OrderState.READY_TO_ORDER
