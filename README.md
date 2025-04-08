# CrewAI Summarizer MCP Server 📝

Um servidor MCP (Multi-Crew Protocol) que utiliza agentes CrewAI para fornecer um serviço de sumarização (resumo) de texto.

## ✨ Features

*   Sumariza textos utilizando agentes CrewAI configuráveis.
*   Permite especificar o tamanho do resumo desejado (curto, médio, longo).
*   Expõe a funcionalidade via protocolo MCP para fácil integração.
*   Utiliza definições personalizáveis de Agentes e Tarefas CrewAI (via arquivos `agents.yaml` e `tasks.yaml`).
*   Pode ser configurado para usar diferentes LLMs suportados pelo CrewAI (requer ajuste no código e variáveis de ambiente).

## 🛠️ Tool

### summarize

Processa um texto de entrada e retorna um resumo conciso no tamanho especificado.

**Inputs:**

*   `text` (string, **required**): O texto original a ser sumarizado.
*   `length` (string, optional, default: `"medium"`): O tamanho desejado para o resumo. Valores válidos: `"short"`, `"medium"`, `"long"`.

**Output:**

*   `string`: O texto resumido gerado pelo agente CrewAI.

## 🎯 Usage (Casos de Uso)

Esta ferramenta é ideal para:

*   Integrar capacidade de sumarização de IA em outros fluxos de trabalho ou ferramentas.
*   Obter rapidamente a essência de documentos longos.
*   Construir aplicações que necessitem de componentes de sumarização dinâmica.
*   Experimentar e expor agentes CrewAI como um microsserviço via MCP.

## 🚀 Setup & Installation

1.  **Pré-requisitos:**
    *   Python >= 3.10, < 3.13
    *   `git`
    *   Recomendado: `uv` (ou `pip` e `venv`)

2.  **Clonar o Repositório:**
    ```bash
    git clone https://github.com/matheus896/crewai-mcp.git # Ou o URL correto do seu repo
    cd crewai-mcp/summarizer_server
    ```

3.  **Criar e Ativar Ambiente Virtual (Recomendado):**
    ```bash
    # Usando venv
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # OU
    .\.venv\Scripts\activate  # Windows

    # Ou se estiver usando uv (ele pode gerenciar o venv automaticamente)
    ```

4.  **Instalar Dependências:**
    ```bash
    # Usando uv
    uv pip install -e .

    # Ou usando pip
    pip install -e .
    ```
    *(O `-e .` instala o pacote em modo editável, o que é útil para desenvolvimento)*

5.  **Configurar Variáveis de Ambiente:**
    *   Crie um arquivo chamado `.env` dentro do diretório `summarizer_server/`.
    *   Adicione sua(s) chave(s) de API para o LLM que você pretende usar. O exemplo em `crew.py` usa Gemini.
        ```dotenv
        # Exemplo para Gemini
        GEMINI_API_KEY=SUA_CHAVE_API_AQUI

        # Exemplo para OpenAI
        # OPENAI_API_KEY=SUA_CHAVE_API_AQUI
        # OPENAI_MODEL_NAME=gpt-4-turbo
        ```
    *   **Importante:** Se você quiser usar um LLM diferente do configurado em `src/summarizer_server/crew.py` (atualmente Gemini), você precisará editar aquele arquivo para importar e instanciar o LLM correto (ex: `ChatOpenAI`, `ChatAnthropic`, etc.) e garantir que as variáveis de ambiente correspondentes estejam no `.env`.

## ▶️ Running the Server

A forma recomendada de iniciar o servidor (usando o script definido em `pyproject.toml`):

```bash
uv run run_crew
```

Alternativamente, se você não estiver usando `uv` ou quiser rodar diretamente com Python (certifique-se que seu ambiente virtual está ativo):

```bash
python src/summarizer_server/main.py
```

O servidor será iniciado e escutará por conexões MCP via `stdio`.

## 🔌 Configuration (Example for MCP Clients like Claude Desktop)

Para usar este servidor com um cliente MCP como o Claude Desktop, você precisa informar ao cliente como executar o servidor. Como este projeto é executado localmente via Python/uv, a configuração apontará para o comando de execução.

**Importante:** O cliente MCP precisa executar o comando a partir do diretório correto (`summarizer_server`) ou ter o ambiente configurado para encontrar o módulo e o arquivo `.env`. O uso de `cwd` (Current Working Directory) na configuração do cliente é altamente recomendado.

**Exemplo usando `uv` (Requer `uv` instalado e acessível no PATH):**

Adicione isto ao seu arquivo de configuração do cliente MCP (ex: `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "crewai-summarizer": {
      "command": "uv",
      "args": [
        "run",
        "run_crew"
      ],
      // MUITO IMPORTANTE: Ajuste este caminho para o local onde você clonou o repo
      "cwd": "/caminho/completo/para/matheus896-crewai-mcp/summarizer_server"
    }
  }
}
```

**Exemplo usando `python` (Requer Python e o pacote instalado no ambiente virtual):**

```json
{
  "mcpServers": {
    "crewai-summarizer": {
       // Pode precisar ser o caminho completo para o python do venv
      "command": "python",
      "args": [
        "-m",
        "summarizer_server.main"
      ],
      // MUITO IMPORTANTE: Ajuste este caminho
      "cwd": "/caminho/completo/para/matheus896-crewai-mcp/summarizer_server"
    }
  }
}
```

## 📜 License

Este projeto é licenciado sob a MIT License. Veja o arquivo `LICENSE` (se existir no repositório) para mais detalhes.

---

**Observações:**

*   Substitua `/caminho/completo/para/matheus896-crewai-mcp/summarizer_server` pelo caminho real onde o diretório `summarizer_server` está localizado na sua máquina ao configurar o cliente MCP.
*   Adicione um arquivo `LICENSE` ao seu repositório se ainda não tiver um (o MIT é uma escolha comum e permissiva).
*   Certifique-se de que o nome do repositório (`matheus896/crewai-mcp`) esteja correto nos exemplos.
