# src/summarizer_server/server.py
from typing import Literal
from mcp.server.fastmcp import FastMCP

# Importa as instâncias das crews
from summarizer_server.crew import summarizer_crew_instance
from summarizer_server.research_crew import research_crew_instance

# Instancia o servidor MCP
mcp = FastMCP("Multi-tool-Server")

@mcp.tool()
def summarize(text: str, length: Literal["short", "medium", "long"] = "medium") -> str:
    """
    Summarizes the provided text to the specified length (short, medium, or long).
    """
    # Cria o dicionário de inputs para a crew
    inputs = {'text': text, 'length': length}

    # Executa a crew com os inputs fornecidos
    # A instância da crew é importada de crew.py
    try:
        result = summarizer_crew_instance.kickoff(inputs=inputs)
        # Retorna a saída bruta da última tarefa da crew
        # CrewOutput tem o atributo 'raw' que contém a string final
        raw_output = getattr(result, 'raw', str(result))
        return raw_output
    except Exception as e:
        # Adicionando um tratamento de erro básico similar ao research
        print(f"[ERROR] Erro ao sumarizar: {e}") # Log simples para o console do servidor
        return f"Erro ao sumarizar: {str(e)}"


@mcp.tool()

def research(topic: str) -> str:
    """
    Pesquisa na web sobre um tópico específico usando uma AI crew com a ferramenta Serper.
    Input: 'topic' (string) - O tópico a ser pesquisado.
    Output: Um resumo da pesquisa (string).
    """
    
    inputs = {'topic': topic}
    try:
        
        result = research_crew_instance.kickoff(inputs=inputs)
        raw_output = getattr(result, 'raw', str(result))
        
        return raw_output
    except Exception as e:
        
        # Adicionando um log simples para o console do servidor em caso de erro
        print(f"[ERROR] Erro ao pesquisar sobre '{topic}': {e}")
        return f"Erro ao pesquisar sobre '{topic}': {str(e)}"
