import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def get_report_from_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=2048,
    )
    return response.choices[0].message["content"]
