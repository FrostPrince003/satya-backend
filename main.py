from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fakenewscrew import analyze_news_article

app = FastAPI(
    title="Fake News Verification API",
    description="""
    An API endpoint to analyze news articles for factual accuracy, political context, 
    media bias, and public sentiment using a crew of AI agents.
    """
)

# Configure allowed origins (adjust these to match your frontend URL)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    # Add other allowed origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # you can also use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],    # allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],    # allow all headers
)

class Query(BaseModel):
    query: str = Field(..., description="The news article content or headline to be verified.")

@app.get("/", summary="Root Endpoint", description="Simple hello world endpoint to check if the API is running.")
def read_root():
    return {"Hello": "World"}

@app.post("/verify", summary="Verify News Article", response_description="Structured JSON response containing analysis reports.")
async def verify(query: Query):
    try:
        result = analyze_news_article(query.query)
        return result
    except Exception as e:
        print(f"Error during news analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing news article: {str(e)}")
