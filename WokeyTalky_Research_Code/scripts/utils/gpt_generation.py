import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]


from openai import OpenAI
client = OpenAI()

def get_response_gpt(prompt, model_name):
    completion = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=256,
    temperature=0
    )

    return completion.choices[0].message.content