import asyncio

from agents import Runner

from restaurant_agents import triage_agent

async def main():
    result = await Runner.run(triage_agent, "Good evening, I would like to order some food.")
    print(result.final_output)


if __name__ == '__main__':
    asyncio.run(main())