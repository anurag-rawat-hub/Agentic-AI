from dotenv import load_dotenv
import speech_recognition as sr
from groq import Groq
import os

load_dotenv()

# Groq Client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def main():
    r = sr.Recognizer()   # Speech to text

    with sr.Microphone() as source: # Mic Access
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        print("Speak something........")
        try:
            audio = r.listen(source)

            print("Processing Audio...(STT)")
            stt = r.recognize_google(audio)

            print("You said:", stt)

            SYSTEM_PROMPT = """
                You are an expert voice agent. You are given the transcript of what user has said using voice.
                You need to output as if you are a voice agent and whatever you speak will be converted back
                to audio using AI and played back to user. Keep your responses concise and conversational.
            """
            
            # Groq uses the OpenAI-compatible chat completions format
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # You can also use "mixtral-8x7b-32768" or "llama3-70b-8192"
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": stt} # <--- Passing the actual voice transcript here
                ]
            )

            print("AI Response:", response.choices[0].message.content)
            
        except sr.UnknownValueError:
            print("Error: Could not understand the audio. Please speak louder.")
        except sr.RequestError as e:
            print(f"Error: Could not request results from STT service; {e}")

if __name__ == "__main__":
    main()