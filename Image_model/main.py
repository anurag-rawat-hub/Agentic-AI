from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Generate a caption for this image in about 50 words",
        types.Part.from_uri(
            file_uri="https://png.pngtree.com/png-clipart/20240416/original/pngtree-developers-are-coding-programs-on-computers-programmers-are-analyzing-data-png-image_14867886.png",
            mime_type="image/png",
        ),
    ],
)

print("AI:", response.text)