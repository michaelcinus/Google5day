from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types

# Config globale
retry_config = types.HttpRetryOptions(attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 503, 504])

# Agente ricercatore
research_agent = Agent(
    name="ResearchAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""Sei un agente di ricerca specializzato. 
    Il tuo unico compito è utilizzare il tool google_search per trovare 2-3 informazioni rilevanti
    sull'argomento in questione e presentare i risultati con citazioni.""",
    tools=[google_search],
    output_key="research_findings",  
)

# Agente riassuntivo
summarizer_agent = Agent(
    name="SummarizerAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""Leggi i risultati della ricerca forniti: {research_findings}
Crea un riepilogo conciso sotto forma di elenco puntato con 3-5 punti chiave.""",
    output_key="final_summary",
)

# Router Agent
root_agent = Agent(
    name="ResearchCoordinator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""Sei un coordinatore di ricerca. Il tuo obiettivo è rispondere alla domanda dell'utente orchestrando un flusso di lavoro.
    1. Innanzitutto, DEVI chiamare lo strumento `ResearchAgent` per trovare informazioni rilevanti sull'argomento fornito dall'utente.
    2. Successivamente, dopo aver ricevuto i risultati della ricerca, DEVI chiamare lo strumento `SummarizerAgent` per creare un riepilogo conciso.
    3. Infine, presenta il riepilogo finale in modo chiaro all'utente come risposta.""",
    tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
)

