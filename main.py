# from fastapi import FastAPI
# from pydantic import BaseModel
# from fakenewscrew import analyze_news_article
# import json

# app = FastAPI()

# class Query(BaseModel):
#     query: str

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.post("/verify")
# def verify(query: Query):
#     # Call the analyze_news_article function with the user's query
#     result = analyze_news_article(query.query)
    
#     # Return the structured result as a JSON response
#     return result


from fastapi import FastAPI, HTTPException # Import Field
from pydantic import BaseModel, Field

# Assuming fakenewscrew.py is in the same directory
from fakenewscrew import analyze_news_article

app = FastAPI(title="Fake News Verification API", description="""
An API endpoint to analyze news articles for factual accuracy, political context, 
media bias, and public sentiment using a crew of AI agents.
""") # Added title and description for API docs

class Query(BaseModel):
    query: str = Field(..., description="The news article content or headline to be verified.") # Added description using Field

@app.get("/", summary="Root Endpoint", description="Simple hello world endpoint to check if the API is running.") # Added summary and description for API docs
def read_root():
    return {"Hello": "World"}

@app.post("/verify", summary="Verify News Article", response_description="Structured JSON response containing analysis reports.") # Added summary, description and response_description for API docs
async def verify(query: Query): # Made endpoint async
    # try:
    #     # Call the analyze_news_article function with the user's query
        result = analyze_news_article(query.query) # Call analyze_news_article using await if it's made async
        return result
    # except Exception as e:
    #     # Log the error for debugging (optional, but good practice)
    #     print(f"Error during news analysis: {e}")
    #     print(e)
    #     # Return an HTTP error response with more detail
    #     raise HTTPException(status_code=500, detail=f"Error analyzing news article: {str(e)}") # Include error details