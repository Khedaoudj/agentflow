# 1. Les imports
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic 
from langchain_core.tools import tool 
from langgraph.graph import StateGraph, MessagesState, START 
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# 2. L'outil 
@tool 
def get_balance(client_id: int) -> str:
    """Donne le solde du compte bancaire d'un client à partir de son identifiant."""
    soldes = {1: 1250.50, 2: 87.30}
    return f"{soldes.get(client_id, 0)} €"

# 3. Le cerveau 
llm = ChatAnthropic(model="claude-haiku-4-5")
llm_avec_outils = llm.bind_tools([get_balance])

# 4. La fonction de la case "llm"
def appeler_llm(state: MessagesState):
    return {"messages": [llm_avec_outils.invoke(state["messages"])]}

# 5. Le graphe : cases, flèches, compilation
graphe = StateGraph(MessagesState)
graphe.add_node("llm", appeler_llm)
graphe.add_node("tools", ToolNode([get_balance]))

graphe.add_edge(START, "llm")
graphe.add_conditional_edges("llm", tools_condition)
graphe.add_edge("tools", "llm")

agent = graphe.compile()

# 6. Lancer l'agent
resultat = agent.invoke({"messages": [("user", "Quel est le solde du client 1 ?")]})
print(resultat["messages"][-1].content)