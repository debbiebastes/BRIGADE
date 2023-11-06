# Import modules needed for OpenAI API communication
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
print('Response:\n%s ' %response)