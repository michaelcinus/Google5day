from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
import asyncio

# Simulazione tool MCP esterno (fai return di "immagini" mock)
def mcp_image_tool(num_images: int, prompt: str, tool_context: ToolContext):
    BULK_THRESHOLD = 1
    def generate_images(n, prompt):
        return [f"[IMAGE: {prompt}_{i}]" for i in range(n)]
    # Se richiesta normale: auto-approva
    if num_images <= BULK_THRESHOLD:
        return {"status": "approved", "images": generate_images(num_images, prompt)}
    # Se richiesta bulk, serve conferma utente
    if not getattr(tool_context, "tool_confirmation", None):
        tool_context.request_confirmation(
            hint=f"Vuoi davvero generare {num_images} immagini con prompt '{prompt}'? (bulk)",
            payload={"num_images": num_images, "prompt": prompt}
        )
        return {"status": "pending", "message": "In attesa di approvazione per bulk image"}
    # Se ripreso e confermato
    if tool_context.tool_confirmation.confirmed:
        return {"status": "approved", "images": generate_images(num_images, prompt)}
    else:
        return {"status": "rejected", "message": "Richiesta bulk rifiutata"}

# Definisci l’agent con il tool esterno MCP e best practice per conferme
root_agent = LlmAgent(
    name="image_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="Genera immagini (MCP tool). Se richiesta bulk, chiedi conferma all’utente.",
    tools=[mcp_image_tool]
)