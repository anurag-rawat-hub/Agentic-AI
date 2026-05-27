from google import genai
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(
    api_key=api_key
)

# Embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_db=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)

def process_query(query:str):
    print("Searching results ",query)
    search_results=vector_db.similarity_search(query=query)

    context="\n\n\n".join([f"Page Content:{result.page_content} \n Page Number: {result.metadata['page_label']} \n File Location: {result.metadata['source']}"
    for result in search_results])

    SYSTEM_PROMPT=f"""You are a helpful AI assistant who answers user query based on the available context retrieved from a PDF file alog with page_contents and page number
    You should only answer the user based on the following context and navigate the user to open the right page number to know more.

    Context:
    {context}
    """

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"{SYSTEM_PROMPT}\n\nUser: {query}"
    )
    print("AI:", response.text)
    return response.text

