from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from crewai import LLM
from crewai_tools import SerperDevTool
import os
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")

# llm = LLM(
#     model="groq/mixtral-8x7b-32768",
#     temperature=0.7,
    
# )

llm = ChatOpenAI(
    model="ollama/llama3.2",
    base_url="http://localhost:11434/v1",
)
# llm = LLM(
#     model="gpt-4o-mini",
# )

search_tool = SerperDevTool()

