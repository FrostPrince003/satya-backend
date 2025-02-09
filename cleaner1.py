import re
import json

def extract_sources(text):
    """
    Extracts a list of sources from the text. Searches for a block starting with
    "Sources:" or "Sources Consulted:" and returns a list of dictionaries with the source text and URL.
    """
    sources = []
    # Look for the sources block
    match = re.search(r'(Sources(?: Consulted)?:)(.*)', text, re.DOTALL)
    if match:
        sources_text = match.group(2)
        for line in sources_text.splitlines():
            line = line.strip()
            if line.startswith("-") or line.startswith("*"):
                # Extract URL if present
                url_match = re.search(r'\((https?://[^\)]+)\)', line)
                url = url_match.group(1) if url_match else ""
                # Clean up the source text by removing the bullet marker
                source_text = line.lstrip("-* ").strip()
                sources.append({"source_text": source_text, "url": url})
    return sources

def structure_results1(results):
    """
    Transforms the multi-agent output (the 'results' variable) into a structured JSON object.
    
    Expected mapping:
      - Fact-Checking Agent → "fact_checking"
      - Political Analyst Agent → "political_analysis"
      - Media Bias Analyst Agent → "media_bias"
      - Public Sentiment Analyst Agent → "public_sentiment"
      - Summary Agent → "combined_summary"
    
    Each section includes:
      - 'agent': Name of the agent.
      - 'response': The agent's text response (with sources removed for clarity).
      - 'sources': A list of extracted sources (if any).
      - For the combined summary, an additional 'final_verdict' key is added.
    """
    structured = {}
    # Mapping agent names to keys that can be used by your frontend
    agent_mapping = {
        "Fact-Checking Agent": "fact_checking",
        "Political Analyst Agent": "political_analysis",
        "Media Bias Analyst Agent": "media_bias",
        "Public Sentiment Analyst Agent": "public_sentiment",
        "Summary Agent": "combined_summary"
    }
    
    for task in results:
        task_dict = task[0]
        agent = task_dict.get("agent", "Unknown Agent")
        key = agent_mapping.get(agent, agent)
        raw_text = task.get("raw", "").strip()
        
        # Extract any sources present
        sources = extract_sources(raw_text)
        
        # Remove the sources block from the main response text
        if "Sources:" in raw_text:
            response = raw_text.split("Sources:")[0].strip()
        elif "Sources Consulted:" in raw_text:
            response = raw_text.split("Sources Consulted:")[0].strip()
        else:
            response = raw_text
        
        structured[key] = {
            "agent": agent,
            "response": response,
            "sources": sources
        }
        
        # For the combined summary, try to determine a final verdict
        if key == "combined_summary":
            if "True" in raw_text:
                structured[key]["final_verdict"] = "Not Fake"
            elif "False" in raw_text:
                structured[key]["final_verdict"] = "Fake"
            else:
                structured[key]["final_verdict"] = "Undetermined"
    
    return structured

# Example of how you would call this function:

