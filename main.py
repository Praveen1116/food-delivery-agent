import asyncio
from tasks.task1_manager import main as run_task1
from tasks.task2_blackboard import main as run_task2


async def main():
    print("=" * 40)
    print("Running Task 1: Manager")
    print("=" * 40)
    await run_task1()

    print("\n" + "=" * 40)
    print("Running Task 2: Blackboard")
    print("=" * 40)
    await run_task2()


if __name__ == "__main__":
    asyncio.run(main())

