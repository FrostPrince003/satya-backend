from langchain.tools import tool
from crewai import Agent, Task, Crew, Process
import requests
from bs4 import BeautifulSoup
import re

@tool
def crawl_website() -> str:
    """
    Crawls a website given its sitemap URL and returns all page URLs.
    The sitemap URL should be passed as the first part of a string, separated by a pipe '|'.
    """
    sitemap_url = "https://aliirz.com/sitemap.xml"  # Assuming the first argument is the sitemap URL
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    return '\n'.join(urls)

@tool
def analyze_content_for_typos_and_seo(urls) -> str:
    """
    Analyzes the content of web pages for typos and bad SEO practices.
    Returns a bullet list in Markdown format.
    """
    # Dummy implementation for demonstration. In practice, this should
    # use a real typo detection and SEO analysis library or API.
    markdown_output = "# Website Analysis Report\n\n"
    for url in urls.split('\n'):
        markdown_output += f"- Analyzed {url}: Found X typos, Y SEO issues\n"
    return markdown_output

# Define the agents
web_crawler = Agent(
    role='Web Crawler',
    goal='Crawl the website to find all page URLs.',
    backstory=("Experienced in web crawling and data extraction, this agent has "
               "a history of efficiently gathering data from websites while adhering to ethical guidelines."),
    verbose=True,
    tools=[crawl_website]
)

seo_analyst = Agent(
    role='SEO Analyst',
    goal='Analyze the website for typos and SEO issues.',
    backstory=("With a deep understanding of SEO practices and content optimization, "
               "this agent specializes in identifying and rectifying typos and SEO inefficiencies."),
    verbose=True,
    tools=[analyze_content_for_typos_and_seo]
)

# Create tasks for each agent
task_crawl = Task(
    description='Crawl the website using its sitemap.',
    agent=web_crawler
)

task_analyze = Task(
    description='Analyze the crawled web pages for typos and SEO issues.',
    agent=seo_analyst
)

# Assemble the crew
crew = Crew(
    agents=[web_crawler, seo_analyst],
    tasks=[task_crawl, task_analyze],
    process=Process.sequential,
    verbose=True
)

# Execute the crew to start the analysis
sitemap_url = "https://aliirz.com/sitemap.xml"  # Replace with the actual sitemap URL
result = crew.kickoff()
print(result)
