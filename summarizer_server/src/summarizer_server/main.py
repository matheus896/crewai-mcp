# summarizer_server/main.py
import sys
from pathlib import Path

# Garante que o diretório 'src' esteja no path para importações corretas
# (útil se você rodar este script diretamente fora do 'uv run')
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Importa a instância do servidor MCP de server.py
from .server import mcp

def run():
    """Runs the MCP server using stdio transport."""
    print("Starting Summarizer MCP Server on stdio...", file=sys.stderr)
    # Carrega variáveis de ambiente do .env (se existir)
    from dotenv import load_dotenv
    load_dotenv()
    mcp.run(transport='stdio')

# Permite rodar o script diretamente com 'python src/summarizer_server/main.py'
if __name__ == "__main__":
    run()