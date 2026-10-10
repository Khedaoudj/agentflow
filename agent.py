from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool 
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

@tool
def get_balance(client_id: int) -> str:
    """Donne le solde du compte bancaire d'un client à partir de sont identifiant."""
    soldes = {1: 1250.50, 2: 87.30}
    return f"{soldes.get(client_id, 0)} €"

outils = {"get_balance": get_balance}

llm = ChatAnthropic(model="claude-haiku-4-5")
llm_avec_outils = llm.bind_tools([get_balance])

messages = [HumanMessage("Quel est le solde du client 1 ?")]

while True: 
    reponse = llm_avec_outils.invoke(messages)
    messages.append(reponse)

    if not reponse.tool_calls:
        break

    for appel in reponse.tool_calls:
        outil = outils[appel["name"]]
        resultat = outil.invoke(appel["args"])
        messages.append(ToolMessage(content=resultat, tool_call_id=appel["id"]))
  
print(reponse.content)
