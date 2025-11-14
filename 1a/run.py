import asyncio
from agent.agent import root_agent
from google.adk.runners import InMemoryRunner

async def main():
    runner = InMemoryRunner(agent=root_agent)
    print("Chiedi qualcosa all'agente (Invio vuoto per uscire): ")
    while True:
        query = input("> ")
        if not query:
            break
        response = await runner.run_debug(query)
        print(response) 

if __name__ == "__main__":
    asyncio.run(main())
