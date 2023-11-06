import os
import requests

# Token from your HF account, set as an environment variable in your machine.
api_token = os.getenv("HF_API_TOKEN")  

# Your Hugging Face endpoint URL
API_URL = "https://l3ehn05l5flgwj30.us-east-1.aws.endpoints.huggingface.cloud"

# Headers expected by the Hugging Face endpoint
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
}

# Call the Generative AI Service
def call_ai(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1024,
            "return_full_text": False,
            "temperature": 0.6,
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['generated_text']

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
print('Response:\n%s ' %response)