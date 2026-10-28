import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agent_framework import WorkflowBuilder, WorkflowContext, executor
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


async def ask(agent, text):
    reply = await agent.run(text)
    return reply.text.strip()


# Allergy specialist agent
allergy_agent = make_agent(
    "allergy",
    "You are an allergy checker. Reply with one word: ALLERGY if the text mentions food allergies, nuts, ingredients, or allergic reactions, otherwise OK."
)


# Workflow executors: start -> allergy_step -> summary_step
@executor(id="start")
async def start(ticket: str, ctx: WorkflowContext[str]) -> None:
    ctx.set_state("ticket", ticket)     # save the ticket on the board
    ctx.set_state("notes", [])          # save an empty "notes" list on the board
    await ctx.send_message("go")


@executor(id="allergy_step")
async def allergy_step(_: str, ctx: WorkflowContext[str]) -> None:
    ticket = ctx.get_state("ticket")
    notes = ctx.get_state("notes")                  # 1. READ the notes
    answer = await ask(allergy_agent, ticket)
    notes = notes + ["allergy: " + answer]          # 2. ADD "allergy: ALLERGY" or "allergy: OK"
    ctx.set_state("notes", notes)                   # 3. WRITE them back
    await ctx.send_message("go")


@executor(id="summary_step")
async def summary_step(_: str, ctx: WorkflowContext) -> None:
    ticket = ctx.get_state("ticket")
    notes = ctx.get_state("notes")
    print("Ticket:", ticket)
    print("Notes:", ", ".join(notes))
    await ctx.yield_output("Ticket: " + ticket + "\nNotes: " + ", ".join(notes))


# Build the workflow
board_flow = (WorkflowBuilder(start_executor=start)
              .add_edge(start, allergy_step)
              .add_edge(allergy_step, summary_step)
              .build())


async def main():
    ticket = "I have a nut allergy and my salad had peanuts in it!"
    await board_flow.run(ticket)


if __name__ == "__main__":
    asyncio.run(main())

