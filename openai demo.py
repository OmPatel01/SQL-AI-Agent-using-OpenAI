import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example of using the new API (chat model)
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or your preferred model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ],
        max_tokens=50
    )
    print("Response:", response['choices'][0]['message']['content'])
except Exception as e:
    print("Error:", e)
