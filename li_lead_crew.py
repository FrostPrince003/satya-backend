import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool

# Set environment variables for API keys
os.environ["SERPER_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

# LinkedIn Researcher Agent
linkedin_researcher = Agent(
    role='Researcher',
    goal='Extract information about a person, their job, and workplace from the url',
    backstory=(
        "As a dedicated researcher, you specialize in gathering detailed "
        "professional profiles from LinkedIn to enable personalized outreach."
    ),
    tools=[ScrapeWebsiteTool(website_url='https://www.linkedin.com/in/faisal-shahid-54b1b720/')],
    memory=True
)

# Message Drafting Agent
message_drafter = Agent(
    role='Communications Specialist',
    goal='Draft a personalized invitation message based on the LinkedIn data gathered',
    backstory=(
        "Armed with a deep understanding of Botterfly, you craft tailored messages "
        "that highlight how Botterfly’s features specifically address the challenges "
        "and needs of the recipient."
    ),
    memory=True,
    context={
        'botterfly_description': (
            "Botterfly is a SaaS startup focused on improving project management "
            "processes through automation and AI-driven insights. It integrates with "
            "tools like Jira, Asana, Monday, and Slack, focusing on task allocation, "
            "project setup, and workload optimization."
        ),
        'botterfly_features': (
            "Key features include transforming rough notes into organized project plans, "
            "automating weekly reports, and providing predictive insights for continuous "
            "improvement. Designed to save time and enhance productivity, especially for "
            "project managers and team leads in software and digital marketing fields."
        )
    }
)

# Research Task
research_task = Task(
    description='Scrape LinkedIn profile data for relevant professional information.',
    expected_output='A dictionary with person name, job, and workplace details.',
    agent=linkedin_researcher
)

# Drafting Task
drafting_task = Task(
    description=(
        "Use the information from the LinkedIn profile to draft a personalized "
        "invitation message highlighting how Botterfly can benefit the recipient, "
        "leveraging detailed product context."
    ),
    expected_output='A personalized message ready to be sent.',
    agent=message_drafter
)

# Crew Configuration
botterfly_crew = Crew(
    agents=[linkedin_researcher, message_drafter],
    tasks=[research_task, drafting_task],
    process=Process.sequential
)

# Example usage
inputs = {'profile_url': 'https://www.linkedin.com/in/faisal-shahid-54b1b720/'}
result = botterfly_crew.kickoff(inputs)
print(result)
