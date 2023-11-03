# Import modules needed for OpenAI API communication
import os
import openai

# Read local .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# Set the API key from the environment variable
openai.api_key  = os.getenv('OPENAI_API_KEY')

# Call the Generetive AI Service like OPENAI
def call_ai(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    temperature=0.5
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return {
        'body': response.choices[0].message["content"],
        'context': {
            'ChatGPT model': response.model,
            'temperature': temperature,
            'ChatGPT token usage': response.usage,
        }
    }

# Create a prompt to send to the Generative AI Service
product_name = "Kyushu Calm Lounge Sofa"
review_text="""
The quality of the fabric on this couch is okay, but it's not the most comfortable seating I've experienced. It looks nice in my living room, though.
"""

prompt = f"""Here is a product review from a customer, which is delimited with triple backticks.

Product Name: {product_name}
Review text: 
```
{review_text}
```

What is the sentiment of that product review?
Identify the product being reviewed.
Enumerate the positive and negative aspects of the product review.
The response should have the following elements:
        - Product name
        - Review Sentiment (Positive/Negative/Neutral)
        - Positive comments about the product (Enumerate)
        - Negative comments about the product (Enumerate)
"""

# Do something with the AI response
print('Prompt: %s' %prompt)
response = call_ai(prompt)
print('Response:\n%s ' %response['body'])
print('\nContext:\n%s ' %response['context'])