# src/summarizer_server/research_crew.py
import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

# Importa a ferramenta Serper
from crewai_tools import SerperDevTool

# Carrega variáveis de ambiente
load_dotenv()

# Configura o LLM (use o mesmo que as outras crews ou defina um específico)
# Exemplo com Gemini (garanta que GEMINI_API_KEY está no .env)
llm = LLM(model='gemini/gemini-2.0-flash-001')
#llm = LLM(model="gpt-4o") # Exemplo OpenAI

# Garanta que SERPER_API_KEY está no .env
search_tool = SerperDevTool()

@CrewBase
class ResearchCrew():
    """ResearchCrew crew"""
    agents_config = 'config/researcher_agents.yaml'
    tasks_config = 'config/researcher_tasks.yaml'

    @agent
    def web_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['web_researcher'],
            tools=[search_tool],  # <= Associa a ferramenta Serper aqui!
            llm=llm,
            verbose=False
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.web_researcher() # Associa a tarefa ao agente
        )

    @crew
    def crew(self) -> Crew:
        """Cria a ResearchCrew"""
        return Crew(
            agents=[self.web_researcher()],
            tasks=[self.research_task()],
            process=Process.sequential,
            verbose=False,
        )

# Cria a instância da crew pronta para importação
research_crew_instance = ResearchCrew().crew()