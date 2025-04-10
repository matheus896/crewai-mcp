# CrewAI Multi-Tool MCP Server (Summarizer & Researcher) 📝🔍

Um servidor MCP (Multi Context Protocol) que utiliza múltiplos agentes CrewAI para fornecer serviços de **sumarização (resumo) de texto** e **pesquisa web**.

## ✨ Features

*   **Sumarização:** Sumariza textos utilizando agentes CrewAI configuráveis, permitindo especificar o tamanho do resumo (curto, médio, longo).
*   **Pesquisa Web:** Realiza pesquisas na internet sobre tópicos específicos usando um agente CrewAI e a ferramenta `SerperDevTool`.
*   **Exposição via MCP:** Expõe ambas as funcionalidades como `tools` distintos via protocolo MCP para fácil integração.
*   **Configuração Flexível:** Utiliza definições personalizáveis de Agentes e Tarefas CrewAI (via arquivos `.yaml`) para cada funcionalidade.
*   **Suporte a LLMs:** Pode ser configurado para usar diferentes LLMs suportados pelo CrewAI (requer ajuste no código e variáveis de ambiente).

## 🛠️ Tools Expostos via MCP

### 1. summarize

Processa um texto de entrada e retorna um resumo conciso no tamanho especificado.

**Inputs:**

*   `text` (string, **required**): O texto original a ser sumarizado.
*   `length` (string, optional, default: `"medium"`): O tamanho desejado para o resumo. Valores válidos: `"short"`, `"medium"`, `"long"`.

**Output:**

*   `string`: O texto resumido gerado pelo agente CrewAI de sumarização.

### 2. research

Pesquisa na web sobre um tópico específico usando uma AI crew com a ferramenta Serper.

**Inputs:**

*   `topic` (string, **required**): O tópico a ser pesquisado.

**Output:**

*   `string`: Um resumo dos resultados da pesquisa gerado pelo agente CrewAI de pesquisa.

## 🎯 Usage (Casos de Uso)

Este servidor multi-tool é ideal para:

*   Integrar capacidades de sumarização e pesquisa de IA em outros fluxos de trabalho ou ferramentas.
*   Obter rapidamente a essência de documentos longos ou informações sobre um tópico.
*   Construir aplicações que necessitem de componentes dinâmicos de sumarização e pesquisa.
*   Experimentar e expor diferentes funcionalidades CrewAI como microsserviços distintos via MCP a partir de um único servidor.

## 🚀 Setup & Installation

1.  **Pré-requisitos:**
    *   Python >= 3.10, < 3.13
    *   `git`
    *   Recomendado: `uv` (ou `pip` e `venv`)

2.  **Clonar o Repositório (se ainda não o fez):**
    ```bash
    git clone https://github.com/matheus896/crewai-mcp.git
    cd crewai-mcp/summarizer_server
    ```
    *(Se você já clonou e está no diretório `summarizer_server`, pule esta etapa)*

3.  **Criar e Ativar Ambiente Virtual (Recomendado):**
    ```bash
    # Usando venv (se ainda não ativo)
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # OU
    .\.venv\Scripts\activate  # Windows

    # Ou se estiver usando uv (ele pode gerenciar o venv automaticamente)
    ```

4.  **Instalar/Atualizar Dependências:**
    ```bash
    # Usando uv
    uv pip install -e .

    # Ou usando pip
    pip install -e .
    ```
    *(Verifique se `crewai_tools` foi instalado, pois `crewai[tools]` está no `pyproject.toml`)*

5.  **Configurar Variáveis de Ambiente:**
    *   **Crie um arquivo chamado `.env`** dentro do diretório `summarizer_server/` (se ainda não existir).
    *   **Adicione suas chaves de API necessárias:**
        *   **Chave do LLM:** Necessária para ambas as crews.
        *   **Chave do Serper:** Necessária para o tool `research`.

        ```dotenv
        # Exemplo para Gemini (LLM)
        GEMINI_API_KEY=SUA_CHAVE_API_GEMINI_AQUI

        # Exemplo para OpenAI (LLM)
        # OPENAI_API_KEY=SUA_CHAVE_API_OPENAI_AQUI
        # OPENAI_MODEL_NAME=gpt-4o # Opcional, pode ser definido no código

        # Chave da API Serper (Necessária para o tool 'research')
        SERPER_API_KEY=SUA_CHAVE_API_SERPER_AQUI
        ```
    *   **Importante:**
        *   Se você quiser usar um LLM diferente do configurado em `src/summarizer_server/crew.py` e `src/summarizer_server/research_crew.py` (atualmente Gemini), você precisará editar esses arquivos para importar e instanciar o LLM correto (ex: `ChatOpenAI`, `ChatAnthropic`, etc.).
        *   Certifique-se que a variável de ambiente correspondente ao LLM escolhido esteja definida no `.env`.
        *   **A `SERPER_API_KEY` é obrigatória para que o tool `research` funcione.**

## ▶️ Running the Server

A forma recomendada de iniciar o servidor (usando o script definido em `pyproject.toml`):

```bash
uv run run_crew
```

Alternativamente, se você não estiver usando `uv` ou quiser rodar diretamente com Python (certifique-se que seu ambiente virtual está ativo):

```bash
python src/summarizer_server/main.py
```

O servidor será iniciado e escutará por conexões MCP via `stdio`, oferecendo os tools `summarize` e `research`.

## 🔌 Configuration (Example for MCP Clients like Claude Desktop)

Para usar este servidor com um cliente MCP, você precisa informar ao cliente como executar o servidor.

**Importante:** O cliente MCP precisa executar o comando a partir do diretório correto (`summarizer_server`) ou ter o ambiente configurado para encontrar o módulo e o arquivo `.env`. O uso de `cwd` (Current Working Directory) na configuração do cliente é altamente recomendado.

**Exemplo usando `uv` (Requer `uv` instalado):**

Adicione isto ao seu arquivo de configuração do cliente MCP (ex: `claude_desktop_config.json`), ajustando o `cwd` e o nome do servidor (`Multi-tool-Server` conforme definido em `server.py`):

```json
{
  "mcpServers": {
    "crewai-multi-tool": { // Nome para o cliente MCP identificar
      "command": "uv",
      "args": [
        "run",
        "run_crew"
      ],
      // MUITO IMPORTANTE: Ajuste este caminho para o local real
      "cwd": "/caminho/completo/para/matheus896-crewai-mcp/summarizer_server"
    }
  }
}
```

**Exemplo usando `python` (Requer Python e o pacote instalado):**

```json
{
  "mcpServers": {
    "crewai-multi-tool": {
       // Pode precisar ser o caminho completo para o python do venv
      "command": "python",
      "args": [
        "-m",
        "summarizer_server.main" // Aponta para o ponto de entrada
      ],
      // MUITO IMPORTANTE: Ajuste este caminho
      "cwd": "/caminho/completo/para/matheus896-crewai-mcp/summarizer_server"
    }
  }
}
```

**Exemplo para linha de comando no Windows (adaptar para outros OS):**

```json
{
    "crewai-multi-tool-server": { // Nome do servidor no cliente
      "command": "cmd",
      "args": [
        "/c",
        "uv",
        "--directory",
        "C:\\caminho\\completo\\para\\matheus896-crewai-mcp\\summarizer_server", // <-- ALTERE PARA O SEU CAMINHO
        "run",
        "run_crew"
      ],
      "env": {
        // "GEMINI_API_KEY": "SUA_CHAVE_GEMINI_AQUI",
        // "SERPER_API_KEY": "SUA_CHAVE_SERPER_AQUI"
      },
      "transportType": "stdio",
      "disabled": false,
      "autoApprove": [],
      "timeout": 60
    }
}
```

Após conectar, o cliente MCP (como o MCP Inspector ou Claude Desktop) deverá listar os tools `summarize` e `research` como disponíveis a partir deste servidor.

## 📜 License

Este projeto é licenciado sob a MIT License.

---

**Observações:**

*   Substitua `/caminho/completo/para/matheus896-crewai-mcp/summarizer_server` pelo caminho real onde o diretório `summarizer_server` está localizado na sua máquina ao configurar o cliente MCP.
*   Certifique-se de que o nome do repositório (`matheus896/crewai-mcp`) esteja correto nos exemplos.
