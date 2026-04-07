import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

# GitHub Models configuration
client = OpenAI(
    base_url="https://models.inference.ai.azure.com/",
    api_key=os.getenv("GITHUB_TOKEN")
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Xin chào, bạn là ai?"}
    ]
)

print(response.choices[0].message.content) 