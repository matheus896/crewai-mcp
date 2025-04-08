# src/summarizer_server/server.py
from typing import Literal
from mcp.server.fastmcp import FastMCP

# Importa a instância da crew criada em crew.py
# Importa a instância da crew criada em crew.py
# Usando importação absoluta a partir do nome do pacote
from summarizer_server.crew import summarizer_crew_instance

# Instancia o servidor MCP
mcp = FastMCP("SummarizerServer")

@mcp.tool()
def summarize(text: str, length: Literal["short", "medium", "long"] = "medium") -> str:
    """
    Summarizes the provided text to the specified length (short, medium, or long).
    """
    # Cria o dicionário de inputs para a crew
    inputs = {'text': text, 'length': length}

    # Executa a crew com os inputs fornecidos
    # A instância da crew é importada de crew.py
    result = summarizer_crew_instance.kickoff(inputs=inputs)

    # Retorna a saída bruta da última tarefa da crew
    # CrewOutput tem o atributo 'raw' que contém a string final
    return result.raw