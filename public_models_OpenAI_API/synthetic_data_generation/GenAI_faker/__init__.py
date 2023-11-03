# Import modules needed for OpenAI API communications
import openai
import os
import time
import json
from faker import Faker

fake = Faker()
api_key=''

# Call the Generetive AI Service like OPENAI
def call_ai(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    temperature = 0.8
    openai.api_key  = api_key
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

def product_review(payload):
    product =payload.get('Furniture_Name', 'Unknown Product')

    #create product review for each product in the catalog
    product_review = {
        "Product ID": payload.get('Furniture_ID', 'Unknown Product ID'),
        "Product Name": payload.get('Furniture_Name', 'Unknown Product'),
        "Name of Reviewer": fake.name(),
        "Star Rating": fake.pyint(min_value=1, max_value=5),
    }

    prompt = f"""
    Create a sample customer review for the ```{product}```. 
    It can be positive, negative or neutral sentiment given the provided Star Rating.
    ```{product_review['Star Rating']}```
    The response should be in a python dictionary format with the following elements:
    - Product Name
    - Product Review
    """

    try:
        GenAI_review_text = call_ai(prompt)
        product_review['Product Review'] = json.loads(GenAI_review_text['body'])['Product Review']
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
        
    return product_review