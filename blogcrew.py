from crewai import Agent, Task, Process, Crew
from langchain.llms import Ollama
ollama_llm = Ollama(model="openhermes")

# Enter your research topic 
research_topic= "Election technologies around the world and why is pakistan so far behind in adopting them"

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
"""
1. Create agent who works for you as a researcher. Researcher will access information availble over internet to about the topic.
2. Create one more agent who writes about the the content provided by the researcher. 
3. Crete one more agent as review who will review ohe co_llmit . Define agents for resarde fine agents that are going to reseh latest   tools and write a blog about it 

"""
researcher = Agent(
    role="Senior Researcher",
    goal=f"Find the latest topic about {research_topic} on the internet.",
    backstory="""""you are expert in researching about the latest news and information about various topics. 
    """,
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=ollama_llm
)

writer = Agent(
    role=" Technical Writer",
    goal="Write engaging  report about the information provided and use simple english",
    backstory="""You are expert in writing various domai articles. Your articles are engaging and interesting.""",
    verbose=True,
    allow_delegation=True,
    llm=ollama_llm
)
reviewer = Agent(
    role="Expert Writing Critic",
    goal="Review the and identfy potential issues in article draft. Make sure draft has neutral tone and simple english.",
    backstory="""You are expert reviewer with 10 years of exprience in reviewing documents. 
    The make sure that article are interesting and correct information provided.
    """,
    verbose=True,
    allow_delegation=True,
    llm=ollama_llm
)

task_report = Task(
    description="""Conduct a thorough examination of the latest advancements in artificial intelligence (AI) in 2024. 
    Identify the key trends, breakthrough technologies, and potential industry impacts.
 
      Your final product should be a comprehensive analysis report. 
    """,
    agent= researcher,
)

task_blog = Task(
    description=f"""Craft a blog post with a concise and impactful headline, 
    showcasing at least 10 paragraphs that summarize the latest information 
    found online. Engage your audience with a compelling, fun, 
    and informative tone that effectively conveys the technical aspects of the topic in simple terms.
    Highlight specific new, exciting projects, apps, and companies revolutionizing {research_topic}. 
    Employ a clear and concise writing style, avoiding numbered paragraphs, and bolding project and tool names. 
    Ensure that all project, tool, and research paper links are included within the article.
    """,
    agent=writer,
)

task_critique = Task(
    description="""Sharpen the focus of the blog by identifying overly wordy sections and crafting concise alternatives. 
    Ensuring a captivating headline of no more than 40 characters, the blog should encompass at least 3 paragraphs.
    Incorporate specific model, company, and project names, while also providing compelling reasons for readers to 
    delve deeper into each entry. Maintain consistency in linking each paper, project, and company to their respective sources.
    """,
    agent= reviewer,
)

# instantiate crew of agents
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[task_report, task_blog, task_critique],
    verbose=2,
    process=Process.sequential,  # Sequential process will have tasks executed one after the other and the outcome of the previous one is passed as extra content into this next.
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
