import os
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

root_agent = Agent(
    name="assistente_utile",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Un agente semplice che risponde e ragiona.",
    instruction="Sei un assistente utile. Se non sei sicuro usa Google Search.",
    tools=[google_search]
)
