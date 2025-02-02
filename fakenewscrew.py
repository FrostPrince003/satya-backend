from crewai import Agent, Task, Crew, Process
from tools import llm, search_tool
from dotenv import load_dotenv
import os

load_dotenv()

ollama_llm = llm

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Define Agents
fact_checking_agent = Agent(
    role='Fact-Checking Agent',
    goal='Verify the factual accuracy of the news article or statement.',
    backstory='Expert in data verification and fact-checking, skilled in discerning truth from fiction in news reporting.',
    tools=[search_tool],
    verbose=True,
    llm=ollama_llm
)

political_analyst_agent = Agent(
    role='Political Analyst Agent',
    goal='Provide context and political analysis on Pakistan.',
    backstory='Specializes in South Asian geopolitics, focusing on Pakistan.',
    verbose=True,
    llm=ollama_llm
)

media_bias_analyst_agent = Agent(
    role='Media Bias Analyst Agent',
    goal='Assess potential biases in the news source.',
    backstory='Expert in media studies, focusing on detecting biases in news reporting.',
    verbose=True,
    llm=ollama_llm
)

public_sentiment_analyst_agent = Agent(
    role='Public Sentiment Analyst Agent',
    goal='Gauge public reaction to the news.',
    backstory='Skilled in analyzing public opinion and sentiment on social media and online forums.',
    tools=[search_tool],
    verbose=True,
    llm=ollama_llm
)

def analyze_news_article(content):
    # Define Tasks
    fact_checking_task = Task(
        description=f'Analyze the news article: {content} for factual accuracy. Final answer must be a detailed report on factual findings.',
        expected_output='Detailed report on factual findings.',
        agent=fact_checking_agent
    )

    political_analysis_task = Task(
        description=f'Analyze the political context of the news article: {content}. Final answer must include an assessment of the current political situation and its credibility.',
        expected_output='Assessment of the current political situation and its credibility.',
        agent=political_analyst_agent
    )

    media_bias_analysis_task = Task(
        description=f'Evaluate the news source: {content} for biases and report on potential influences on the article\'s narrative. Final answer must include an analysis of media bias.',
        expected_output='Analysis of media bias.',
        agent=media_bias_analyst_agent
    )

    public_sentiment_analysis_task = Task(
        description=f'Analyze public reaction to the news: {content} on social media and forums. Final answer must summarize public sentiment.',
        expected_output='Summary of public sentiment with a clear True or False output. If the claims are true then respond with True, otherwise False.',
        agent=public_sentiment_analyst_agent
    )

    # Create Crew
    crew = Crew(
        agents=[fact_checking_agent, political_analyst_agent, media_bias_analyst_agent, public_sentiment_analyst_agent],
        tasks=[fact_checking_task, political_analysis_task, media_bias_analysis_task, public_sentiment_analysis_task],
        process=Process.sequential,
        verbose=True
    )

    # Kickoff the process
    results = crew.kickoff()

    # Structure the response
    return results
