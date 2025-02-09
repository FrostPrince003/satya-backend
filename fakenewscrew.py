from crewai import Agent, Task, Crew, Process
from tools import llm, search_tool
from dotenv import load_dotenv
from cleaner import structure_results
import os

# Load environment variables
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
    goal='Provide context and political analysis on India.',
    backstory='Specializes in South Asian geopolitics, focusing on India.',
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
verdict_agent = Agent(
    
    role='Verdict Agent',
    goal='Provide a final verdict on the news article. State if it is True or False',
    backstory='Expert in analyzing the credibility of news sources and statements.',
    verbose=True,
    llm=ollama_llm
)
summary_agent = Agent(
    role='Summary Agent',
    goal='Combine all findings into a cohesive narrative that clearly states whether the news is true or false.     ',
    backstory='Expert in synthesizing information from multiple sources to create a clear and concise summary.',
    verbose=True,
    llm=ollama_llm
)

def analyze_news_article(content):
    # Define Tasks with explicit requests for sources, conclusions, and summaries
    fact_checking_task = Task(
        description=f'Analyze the news article: {content} for factual accuracy. '
                    f'Include detailed findings, list all sources consulted, and provide a conclusion about the factual accuracy.',
        expected_output='Detailed report including factual findings, sources consulted with website links, and a clear conclusion (True/False) on whether the claims are accurate.'
                        'You should include the website links at the end if any are considered to create the response.',
        agent=fact_checking_agent
    )

    political_analysis_task = Task(
        description=f'Analyze the political context of the news article: {content}. '
                    f'Include an assessment of the current political situation, list all sources consulted, and provide a conclusion about the credibility of the political narrative.',
        expected_output='Assessment of the current political situation, sources consulted with website links, and a clear conclusion about the credibility of the political narrative.'
                        'You should include the website links at the end if any are considered to create the response.',
        agent=political_analyst_agent
    )

    media_bias_analysis_task = Task(
        description=f'Evaluate the news source: {content} for biases and report on potential influences on the article\'s narrative. '
                    f'Include an analysis of media bias, list all sources consulted, and provide a conclusion about the presence of bias.',
        expected_output='Analysis of media bias, sources consulted with website links, and a clear conclusion about the presence of bias.'
                        'You should include the website links at the end if any are considered to create the response.',
        agent=media_bias_analyst_agent
    )

    public_sentiment_analysis_task = Task(
        description=f'Analyze public reaction to the news: {content} on social media and forums. '
                    f'Summarize public sentiment, list all sources consulted, and provide a conclusion about the overall public sentiment.',
        expected_output='Summary of public sentiment, sources consulted with website links, and a clear conclusion (True/False) about whether the claims align with public sentiment.'
                        'You should include the website links at the end if any are considered to create the response.',
        agent=public_sentiment_analyst_agent
    )

    # Final summarization task to combine all findings into a cohesive narrativ
    verdict_task = Task(
        description=f'Provide a final verdict on the news article: {content} based on the combined findings from the Fact-Checking Agent, Political Analyst Agent, Media Bias Analyst Agent, and Public Sentiment Analyst Agent.',
        expected_output=f'A clear final verdict (True/False) on the news article based on the combined findings from all agents.'
                        f'You should generate a score of how much percent of the {content} is actually true or false based on your analysis'
                        f'where if the {content} is completely false you should return 0% and if it is completely true you should return 100%',
        agent=verdict_agent
    )
    summary_task = Task(
        description=f'Combine the findings from the Fact-Checking Agent, Political Analyst Agent, Media Bias Analyst Agent, '
                    f'and Public Sentiment Analyst Agent into a cohesive narrative. Your summary should:'
                    f'- Provide a brief recap of the factual accuracy, political context, media bias, and public sentiment findings.'
                    f'- Clearly state a final verdict: explicitly declare whether the news is "Not Fake" (true) or "Fake" (false).'
                    f'- Include a field named "final_verdict" in your output that contains this decision.'
                    f'- List all sources consulted from all analyses at the end, with website links if available.'
                    f'Your final conclusion should answer: Is the news article accurate or is it fake?',
        expected_output='A concise narrative summarizing the factual accuracy, political context, media bias, and public sentiment, '
                        'along with a clear final verdict (e.g., "final_verdict": "Not Fake" or "final_verdict": "Fake"). '
                        'Include all sources consulted with website links at the end if available.',
        agent=summary_agent
    )

    # Create Crew
    crew = Crew(
        agents=[
            fact_checking_agent,
            political_analyst_agent,
            media_bias_analyst_agent,
            public_sentiment_analyst_agent,
            verdict_agent,
            summary_agent
        ],
        tasks=[
            fact_checking_task,
            political_analysis_task,
            media_bias_analysis_task,
            public_sentiment_analysis_task,
            verdict_task,
            summary_task
        ],
        process=Process.sequential,
        verbose=True
    )

    # Kickoff the process
    results = crew.kickoff()

    # Structure the response
#     parsed_response = parse_response(results)
#     formatted_json = parsed_response.model_dump_json(indent=4)

# # Convert to JSON for sending to the frontend
#     return formatted_json
    # return results
    
    structured_output = structure_results(results)
    return structured_output


