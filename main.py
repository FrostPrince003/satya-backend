from fastapi import FastAPI
from pydantic import BaseModel
from fakenewscrew import analyze_news_article
import json

app = FastAPI()

class Query(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/verify")
def verify(query: Query):
    # Call the analyze_news_article function with the user's query
    result = analyze_news_article(query.query)
    
    # Return the structured result as a JSON response
    return result
