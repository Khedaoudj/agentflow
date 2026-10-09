from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

load_dotenv()

@tool 
def get_balance(client_id: int) -> str:
    """Donne le solde du compte bancaire d'un client à partir de son identifiant."""
    soldes = {1: 1250.50, 2: 87.30}
    return f"{soldes.get(client_id, 0)} €"

llm = ChatAnthropic(model="claude-haiku-4-5")
llm_avec_outils = llm.bind_tools([get_balance])
reponse = llm_avec_outils.invoke("Quel est le solde du client 1 ?")
print(reponse.tool_calls)
