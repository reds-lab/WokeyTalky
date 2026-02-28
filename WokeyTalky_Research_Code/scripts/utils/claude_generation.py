import anthropic
from dotenv import load_dotenv
import os
load_dotenv()
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

def get_response_claude(prompt, model_name):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=ANTHROPIC_API_KEY,
    )
    
    message = client.messages.create(
    model=model_name,
    max_tokens=256,
    temperature=0.0,
    system="",
    messages=[
        {"role": "user", "content": prompt}
    ])
    
    return message.content[0].text

