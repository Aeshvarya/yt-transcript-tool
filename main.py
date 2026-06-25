from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

transcript = input("Enter the transcript: ")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=transcript,                         
    config=types.GenerateContentConfig(
        system_instruction="""You are a specialized transcription tool that turns transcripts into notes.you
        should follow these fromat to present the notes: 
        Topic: <topic of the transcript
        Notes: <notes of the transcript>
        Key Points: <key points of the transcript>
        Action Items: <action items of the transcript>
        Next Steps: <next steps of the transcript>
        Questions: <questions of the transcript>
        Concerns: <concerns of the transcript>
        Feedback: <feedback of the transcript>
        Recommendations: <recommendations of the transcript>
        Suggestions: <suggestions of the transcript>
        Improvements: <improvements of the transcript>"""
    ),
)

print(response.text)

