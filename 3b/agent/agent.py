import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory
from google.adk.runners import Runner
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

root_agent = LlmAgent(
    name="agente_memoria",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    ),
    description="Un agente semplice con memoria di sessione",
    instruction="Sei un assistente utile. Ricorda quello che l'utente ti dice. Usa il tool load_memory per cercare informazioni dal passato.",
    tools=[load_memory],  # ← Aggiunto: tool per cercare nella memoria
)

db_url = "sqlite:///./agent_sessions.db"
session_service = DatabaseSessionService(db_url=db_url)
memory_service = InMemoryMemoryService()  # ← Nuovo: memory service

runner = Runner(
    agent=root_agent,
    app_name="chatbot",
    session_service=session_service,
    memory_service=memory_service,  # ← Aggiunto: connetti il memory service
)
