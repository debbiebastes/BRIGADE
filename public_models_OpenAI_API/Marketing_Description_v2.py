# Import modules needed for OpenAI API communication
import os
import openai

# Read local .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# Set the API key attribute of the GenAI_faker library 
openai.api_key  = os.getenv('OPENAI_API_KEY')

# Call the Generative AI Service like OPENAI
def call_ai(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    temperature=1
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
product_details="""
Product Name: Aspen Dining Table
Style: Rustic
Color Variations: Oak, Maple
Material: Solid Wood
Furniture type: 4-seater Dining Table
Product Category: Dining Room Furniture - Aspen Series
Weight in kilograms: 12
Length in meters: 2
Width in meters: 0.76 
"""

prompt = f"""Generate a compelling and detailed description of a product for a marketing website of a furniture store, in under 100 words. The product name and specifications are provided below which are delimited with triple backticks. 

Product:
```
{product_details}
```

""" 

# Do something with the AI response
print('Prompt: %s' %prompt)
response = call_ai(prompt)
print('Response:\n%s ' %response['body'])
print('\nContext:\n%s ' %response['context'])