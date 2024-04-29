from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from email_campaign.tools.sql_analysis import SQLTools

# Uncomment the following line to use an example of a custom tool
# from realtor.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class EmailCampaignCrew():
	"""Realtor crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[SQLTools.search], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)
	
	@agent
	def email_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['email_writer'],
			verbose=True,
			allow_delegation=False
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file='report.md'
		)
	
	@task
	def email_writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['email_writing_task'],
			agent=self.email_writer(),
			output_file='email.md'
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the Email Campaign crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)