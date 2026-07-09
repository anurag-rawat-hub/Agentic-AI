from dotenv import load_dotenv
from mem0 import Memory
import os
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(
    api_key=api_key
)

config={
    "version":"v1.1",
    "embedder":{
        "provider":"gemini",
        "config":{"api_key":api_key,"model":"models/gemini-embedding-001"}
    },
    "llm":{
        "provider":"gemini",
        "config":{"api_key":api_key, "model":"gemini-2.5-flash"}
    },
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host":"localhost",
            "port": 6333,
            "embedding_model_dims": 768
        }
    }
}

mem_client=Memory.from_config(config)

while True:
    user_query = input("> ")

    if user_query.lower() in ["exit", "quit", "bye"]:
        break

    # Retrieve relevant memories
    memories = mem_client.search(
        #user_id="Anurag",
        query=user_query,
        filters={"user_id":"Anurag"}
    )

    print("Found Memories", memories)

    memory_text = "\n".join(
        memory["memory"] 
        for memory  in memories["results"]
    )
    
    

    prompt = f"""
    You are a helpful AI assitant.
Previous Memories:
{memory_text}

Current User Query:
{user_query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("AI:", response.text)

    mem_client.add(
        user_id="Anurag",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response.text}
        ]
    )

    print("Memory saved.\n")