import json
import os

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# scripts/embed.py
# ----------------
import os
import openai
from dotenv import load_dotenv
from scripts.utils import load_json, save_json


def get_embedding(text, model="text-embedding-3-small"):
    response = openai.Embedding.create(
        input=text,
        model=model
    )
    return response['data'][0]['embedding']


def main():
    # Load API key
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Paths
    raw_path = os.path.join("data", "raw", "network_services.json")
    embed_path = os.path.join("data", "embeddings", "network_services_embeddings.json")

    # Load raw data
    pages = load_json(raw_path)
    all_embeddings = []

    # Generate embeddings for each paragraph
    for page in pages:
        url = page['url']
        for idx, paragraph in enumerate(page['paragraphs']):
            text = f"URL: {url}\nParagraph: {paragraph}"
            embedding = get_embedding(text)
            all_embeddings.append({
                'url': url,
                'paragraph_index': idx,
                'text': paragraph,
                'embedding': embedding
            })

    # Save embeddings
    save_json(all_embeddings, embed_path)
    print(f"Saved {len(all_embeddings)} embeddings to {embed_path}")

if __name__ == '__main__':
    main()

# Usage:
# 1. Place your raw JSON in data/raw/network_services.json
# 2. Populate .env with your OPENAI_API_KEY
# 3. pip install -r requirements.txt
# 4. python scripts/embed.py
