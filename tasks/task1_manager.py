import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agent_framework.openai import OpenAIChatCompletionClient

load_dotenv(find_dotenv(usecwd=True))

# Connection to Groq (OpenAI-compatible)
groq = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SETTINGS = {"temperature": 0}


def make_agent(name, instructions, tools=None):
    if tools:
        return groq.as_agent(name=name, instructions=instructions,
                             tools=tools, default_options=SETTINGS)
    return groq.as_agent(name=name, instructions=instructions,
                         default_options=SETTINGS)


def who_was_called(reply):
    names = []
    for message in reply.messages:
        for item in message.contents:
            if item.type == "function_call":
                names.append(item.name)
    return names


# 1. Two worker agents: delivery and payment
delivery_agent = make_agent(
    "delivery",
    "You are a delivery specialist. You handle late food, delivery delays, and driver issues. Reply in one short sentence."
)

payment_agent = make_agent(
    "payment",
    "You are a payment specialist. You handle charges, payment methods, billing, and refunds. Reply in one short sentence."
)

# 2. Turn each worker into a tool with as_tool
delivery_tool = delivery_agent.as_tool(
    name="ask_delivery",
    description="Ask the delivery specialist about delivery status, late food, and driver delays."
)

payment_tool = payment_agent.as_tool(
    name="ask_payment",
    description="Ask the payment specialist about charges, payment issues, billing, and refunds."
)

# 3. Manager agent using both tools
manager = make_agent(
    "manager",
    "You are a support manager. Never answer yourself. "
    "Pick the right specialist, call their tool, and return their answer.",
    tools=[delivery_tool, payment_tool],
)


async def main():
    ticket = "My food showed up an hour after the promised time"
    reply = await manager.run(ticket)
    print("Task 1:", who_was_called(reply))


if __name__ == "__main__":
    asyncio.run(main())

