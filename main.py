from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("transcript.txt") as f:
    transcript = f.read()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=transcript,                         
    config=types.GenerateContentConfig(
        system_instruction="""you are a specialized transcription tool that turns transcripts into obsdian markdown notes
        you should follow this format to present the notes and Output ONLY the filled template, nothing else:
date: YYYY-MM-DD
category: DSA | Python | AI | Communication | Misc
source: youtube
url: <video link>
channel: <creator>
tags: []
status: learning
---

# Topic — from <channel>

## The one thing to remember
Single sentence. If I read nothing else, this.

## What it covered
2–4 line summary of the video.

## Key points
- Point 1
- Point 2

## My understanding (in my own words)
Re-explain it simply.

## 🧠 Beyond the video (my additions — NOT from the video)
- Clearer explanation / better mental model
- Gaps the video missed
- What's worth learning next + roadmap connection

## How I'd actually use this
Where this applies to my projects / roadmap.

## Links
- [[related-note]]
"""
    ),
)
with open("note.md", "w") as f:
    f.write(response.text)

print("Notes have been generated and saved to note.md")
