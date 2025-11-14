from google.genai import types

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search, AgentTool, ToolContext
from google.adk.code_executors import BuiltInCodeExecutor

def get_fee_for_payment_method(method: str) -> dict:
    """
    Cerca la percentuale di fee per un metodo di pagamento.
    Args: method - Descrizione metodo (es: 'platinum credit card')
    Returns: {'status': 'success', 'fee_percentage': ...} oppure errore
    """
    fee_database = {
        "platinum credit card": 0.02,
        "gold debit card": 0.035,
        "bank transfer": 0.01
    }
    fee = fee_database.get(method.lower())
    if fee is not None:
        return {"status": "success", "fee_percentage": fee}
    else:
        return {"status": "error", "error_message": f"Payment method '{method}' not found"}

def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """
    Cerca il tasso di cambio statico (mock).
    Args: base_currency, target_currency
    Returns: {'status': 'success', 'rate': ...} oppure errore
    """
    rate_database = {
        "usd": {"eur": 0.93, "jpy": 157.50, "inr": 83.58}
    }
    base = base_currency.lower()
    target = target_currency.lower()
    rate = rate_database.get(base, {}).get(target)
    if rate is not None:
        return {"status": "success", "rate": rate}
    else:
        return {"status": "error", "error_message": f"Unsupported currency pair: {base_currency}/{target_currency}"}

root_agent = LlmAgent(
    name="CurrencyAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite"
    ),
    instruction="""
        Sei un assistente per la conversione valuta.
        1. Usa get_fee_for_payment_method() per trovare la fee.
        2. Usa get_exchange_rate() per il tasso di cambio.
        3. Se ricevi errori nei tool, fermati e spiega l’errore.
        4. Calcola l’importo finale dopo la fee e con il cambio.
        5. Riporta il risultato finale e mostra i passaggi usati.
    """,
    tools=[get_fee_for_payment_method, get_exchange_rate]
)
