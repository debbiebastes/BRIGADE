# Import modules needed for OpenAI API communication
import os
import openai

# Read local .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# Your API key from OpenAI
openai.api_key  = os.getenv('OPENAI_API_KEY')

# Call the Generetive AI Service like OPENAI
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What were the main former capitals of Japan?"}
  ]
)

# Do something with the AI response
print(completion.choices[0].message["content"])