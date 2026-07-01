from anthropic import Anthropic
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tool_definitions =[{
    "name": "fetch_transcript",

    "description": "Fetch the transcript of a youtube video when given a url",
    "input_schema": {
        "type": "object",
        "properties": {
            "youtube_url": {
                "type": "string",
                "description": "The url of the youtube video"
            }
        },
        "required": ["youtube_url"]
    }
}
]
def fetch_transcript(youtube_url):
    video_id = youtube_url.split("v=")[1]                         
    ytt_api = YouTubeTranscriptApi()                              
    fetched = ytt_api.fetch(video_id)                            
    transcript = " ".join(snippet.text for snippet in fetched)   
    return transcript



response = client.messages.create(
    tools=tool_definitions,
    model="claude-haiku-4-5",
    max_tokens=1000,
    system="""you are a specialized transcription tool that turns transcripts into obsdian markdown notes
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
""",
    messages=[{"role": "user", "content": "Make a note from this video: https://www.youtube.com/watch?v=596vkrMPWWM"}]

)

for block in response.content:
    if block.type == "tool_use":          
        tool_name = block.name          
        tool_input = block.input    
        tool_id = block.id   

url = tool_input["youtube_url"]              
transcript = fetch_transcript(url)  
messages=[{"role": "user", "content": "Make a note from this video: https://youtube.com/watch?v=abc"},
{"role": "assistant", "content": response.content},
{"role": "user", "content": [
    {"type": "tool_result", "tool_use_id": tool_id, "content": transcript}
]}
]     
final_response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    system="""you are a specialized transcription tool that turns transcripts into obsdian markdown notes
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
""",                 
    tools=tool_definitions,
    messages=messages,          
)

print(final_response.content[0].text)

print("Claude asked for:", tool_name)
print("With URL:", url)
print("My function returned:", transcript)

