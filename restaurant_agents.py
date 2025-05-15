from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel

from data_models import RestaurantMenu

MAIN_MODEL = 'gpt-4o-mini'


class FoodOrderOutput(BaseModel):
    is_food_order: bool
    reasoning: str


guardrail_agent = Agent(
    name='Guardrail_check',
    instructions='Check if user is asking about ordering food, food items on the menu or paying for their order.',
    output_type=FoodOrderOutput,
    model=MAIN_MODEL
)


async def food_order_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx)
    final_output = result.final_output_as(FoodOrderOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_food_order
    )


restaurant_menu_extractor_agent = Agent(
    name='Restaurant Menu Extractor',
    instructions='Extract menu from text or images',
    output_type=RestaurantMenu
)


restaurant_menu_agent = Agent(
    name='Restaurant Menu',
    handoff_description='Specialist agent for explaining the restaurant menu.',
    instructions='You can analyse the menu and provide information to help the customer decide what menu item to choose.',
    model=MAIN_MODEL
)


food_orderer_agent = Agent(
    name='Food Orderer',
    handoff_description='Specialist agent for handling the order of food.',
    instructions='You help the customer choose which items of food to have from the menu.',
    model=MAIN_MODEL
)


billing_agent = Agent(
    name='Billing',
    handoff_description='Specialist agent for handling payment of the bill.',
    instructions='You help the customer with payment of the food order.',
    model=MAIN_MODEL
)


triage_agent = Agent(
    name='Triage Agent',
    instructions='You determine which agent to use based on the customer\'s requests.',
    handoffs=[food_orderer_agent, billing_agent, restaurant_menu_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=food_order_guardrail)
    ],
    model=MAIN_MODEL
)
