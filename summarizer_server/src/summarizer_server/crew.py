# src/summarizer_server/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from dotenv import load_dotenv

# Carregando variáveis de ambiente
load_dotenv()

# configure seu LLM (exemplo com Gemini)
llm = LLM (model = 'gemini/gemini-2.0-flash-001')

@CrewBase
class SummarizerCrew:
    """SummarizerCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def text_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['text_summarizer'],
            llm=llm,
            verbose=False
        )

    @task
    def summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarization_task'],
            agent=self.text_summarizer() # Associa a tarefa ao agente
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SummarizerCrew"""
        return Crew(
            agents=[self.text_summarizer()], # Agentes da crew
            tasks=[self.summarization_task()],   # Tarefas da crew
            process=Process.sequential,
            verbose=False,
        )

# Cria uma instância pronta para ser importada
summarizer_crew_instance = SummarizerCrew().crew()
