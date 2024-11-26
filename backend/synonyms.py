import openai # using an older version of OpenAI to avoid conflicts
from typing import List, Tuple
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY") # hah! you can't find my OpenAI key!

def generate_synonyms(word: str) -> List[str]:
    prompt = f"Generate 10 synonyms for the word '{word}'. Provide a list of words only, separated by commas please."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant whose job is to generate synonyms along with the similarity score"},
                {"role": "user", "content": prompt}
            ]
        )

        # Log the response for debugging
        print("Response:", response)

        synonyms = response['choices'][0]['message']['content'].strip().split(", ")
        return synonyms
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_embedding(text: str) -> List[float]:
    """method to return an embedding for a given text."""
    response = openai.Embedding.create(
        model = "text-embedding-ada-002",
        input = text,
    )
    return response["data"][0]["embedding"]

def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """a method to calculate cosine similarity between two embeddings."""
    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
    norm1 = sum(a * a for a in embedding1) ** 0.5
    norm2 = sum(b * b for b in embedding2) ** 0.5
    return dot_product / (norm1 * norm2)

def sort_synonyms_by_similarity(word: str, synonyms: List[str]) -> List[Tuple[str, float]]:
    """Sort synonyms by similarity to the input word."""
    word_embedding = get_embedding(word)
    synonym_scores = [
        (synonym, calculate_similarity(word_embedding, get_embedding(synonym)))
        for synonym in synonyms
    ]
    return sorted(synonym_scores, key = lambda x: x[1], reverse=True)
