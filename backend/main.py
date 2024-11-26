from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple
import openai
import os
from backend.synonyms import generate_synonyms, sort_synonyms_by_similarity

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class SynonymRequest(BaseModel):
    word: str  # getting the Word input from the user

class SynonymResponse(BaseModel):
    synonyms: List[Tuple[str, float]]  # List of (synonym, similarity_score) tuples

@app.post("/generate-synonyms", response_model=SynonymResponse)
async def generate_synonyms_endpoint(request: SynonymRequest):
    word = request.word

    # the helper functions come to rescue
    synonyms = generate_synonyms(word)
    
    # Sort the synonyms by their respective similarity score
    sorted_synonyms = sort_synonyms_by_similarity(word, synonyms)
    
    # Return the list of synonyms with similarity scores
    return SynonymResponse(synonyms = sorted_synonyms)
