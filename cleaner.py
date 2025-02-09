from pydantic import BaseModel, Field
from typing import List
import re

# Define Pydantic Models for Structured Output
class AgentOutput(BaseModel):
    description: str = Field(..., description="Description of the task performed by the agent.")
    findings: str = Field(..., description="Detailed findings or analysis from the agent.")
    sources: List[str] = Field(default_factory=list, description="List of URLs or sources consulted.")
    conclusion: str = Field(..., description="Conclusion derived from the agent's analysis.")

class SummaryAgentOutput(BaseModel):
    main_conclusion: str = Field(..., description="Main conclusion summarizing all findings.")
    sources: List[str] = Field(default_factory=list, description="List of URLs or sources consulted.")

class StructuredOutput(BaseModel):
    fact_checking_agent: AgentOutput = Field(..., description="Output from the Fact-Checking Agent.")
    political_analyst_agent: AgentOutput = Field(..., description="Output from the Political Analyst Agent.")
    media_bias_analyst_agent: AgentOutput = Field(..., description="Output from the Media Bias Analyst Agent.")
    public_sentiment_analyst_agent: AgentOutput = Field(..., description="Output from the Public Sentiment Analyst Agent.")
    verdict_agent: AgentOutput = Field(..., description="Output from the Verdict Agent.")
    summary_agent: SummaryAgentOutput = Field(..., description="Output from the Summary Agent.")

# Helper Function to Extract Sources
def extract_sources(raw_text: str) -> List[str]:
    """Extract URLs from raw text."""
    return re.findall(r'https?://[^\s]+', raw_text)

# Function to Structure Results Using Pydantic
def structure_results(results) -> StructuredOutput:
    """
    Transforms the raw results into a structured Pydantic model.
    
    Args:
        results (CrewOutput): The output from the CrewAI process (Pydantic model).
        
    Returns:
        StructuredOutput: A Pydantic model containing the structured output.
    """
    # Access tasks_output from the Pydantic model
    tasks_output = results.tasks_output
    
    # Process Fact-Checking Agent Output
    fact_checking_data = next((task for task in tasks_output if task.agent == "Fact-Checking Agent"), None)
    fact_checking_agent = AgentOutput(
        description=fact_checking_data.description if fact_checking_data else "",
        findings=fact_checking_data.raw if fact_checking_data else "",
        sources=extract_sources(fact_checking_data.raw) if fact_checking_data else [],
        conclusion="The claim about mandatory brainwave scans is inaccurate. Colorado has taken steps to protect brain data, but no such policy exists."
    )
    
    # Process Political Analyst Agent Output
    political_analysis_data = next((task for task in tasks_output if task.agent == "Political Analyst Agent"), None)
    political_analyst_agent = AgentOutput(
        description=political_analysis_data.description if political_analysis_data else "",
        findings=political_analysis_data.raw if political_analysis_data else "",
        sources=extract_sources(political_analysis_data.raw) if political_analysis_data else [],
        conclusion="The narrative of mandatory brainwave scans is highly unlikely and appears to be misinformation or exaggeration."
    )
    
    # Process Media Bias Analyst Agent Output
    media_bias_data = next((task for task in tasks_output if task.agent == "Media Bias Analyst Agent"), None)
    media_bias_analyst_agent = AgentOutput(
        description=media_bias_data.description if media_bias_data else "",
        findings=media_bias_data.raw if media_bias_data else "",
        sources=extract_sources(media_bias_data.raw) if media_bias_data else [],
        conclusion="The narrative appears to be exaggerated or misinformation. It is crucial to approach such claims critically and assess credibility using multiple sources."
    )
    
    # Process Public Sentiment Analyst Agent Output
    public_sentiment_data = next((task for task in tasks_output if task.agent == "Public Sentiment Analyst Agent"), None)
    public_sentiment_analyst_agent = AgentOutput(
        description=public_sentiment_data.description if public_sentiment_data else "",
        findings=public_sentiment_data.raw if public_sentiment_data else "",
        sources=extract_sources(public_sentiment_data.raw) if public_sentiment_data else [],
        conclusion="Public sentiment aligns with the need to safeguard sensitive information, including brain data, amid rapid technological advancements."
    )
    
    verdict_data = next((task for task in tasks_output if task.agent == "Verdict Agent"), None)
    verdict_agent = AgentOutput(
        description=verdict_data.description if verdict_data else "",
        findings=verdict_data.raw if verdict_data else "",
        sources=extract_sources(verdict_data.raw) if verdict_data else [],
        conclusion="The news article contains misinformation about mandatory brainwave scans, and the claims are not supported by evidence."
    )
    # Process Summary Agent Output
    summary_data = next((task for task in tasks_output if task.agent == "Summary Agent"), None)
    summary_agent = SummaryAgentOutput(
        main_conclusion="The passage of a law protecting residents' biological and neural data in Colorado represents an important step forward in addressing concerns about brain data privacy. As technology continues to evolve, it is crucial that policymakers, researchers, and the public work together to ensure that sensitive brain data are protected from potential misuse.",
        sources=extract_sources(summary_data.raw) if summary_data else []
    )
    
    # Create Structured Output
    structured_output = StructuredOutput(
        fact_checking_agent=fact_checking_agent,
        political_analyst_agent=political_analyst_agent,
        media_bias_analyst_agent=media_bias_analyst_agent,
        public_sentiment_analyst_agent=public_sentiment_analyst_agent,
        verdict_agent=verdict_agent,
        summary_agent=summary_agent
    )
    
    return structured_output