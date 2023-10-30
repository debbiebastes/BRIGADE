import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def call_ai(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

#test code to get a response from the openai api

prompt = f"""Generate a compelling and detailed description of a product for a marketing website of a furniture store, in under 100 words. The product name and specifications are provided below which are delimited with triple backticks. 

Product:
```
Product Name: Aspen Dining Table
 Style: Rustic
 Color Variations: Oak, Maple
 Material: Solid Wood
 Furniture type: 4-seater Dining Table
 Product Category: Dining Room Furniture - Aspen Series
Weight in kilograms: 12
Length in meters: 2
Width in meters: 0.76 
```

""" 

print('Prompt: %s' %prompt)
response = call_ai(prompt)
print(response) 