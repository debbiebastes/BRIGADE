import json
from typing import Dict, List

#AWS SDK for Python
import boto3
from botocore.config import Config

#Region of our Bedrock endpoint
my_config = Config(region_name = 'us-east-1') 

# Call the Generative AI endpoint
def call_ai(prompt):
    bedrock = boto3.client("bedrock-runtime", config=my_config)
    response = bedrock.invoke_model(
        accept='application/json',
        contentType='application/json',
        modelId='cohere.command-text-v14',
        body=json.dumps({
            "prompt": prompt,
        })
    )
    model_predictions = json.loads(response['body'].read())
    generated_text = model_predictions['generations'][0]['text']
    return generated_text

# Helper function: printing output
def print_instructions(prompt: str, response: str) -> None:
    bold, unbold = '\033[1m', '\033[0m'
    print(f"{bold}> Input{unbold}\n{prompt}\n\n{bold}> Output{unbold}\n{response}\n")

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
response = call_ai(prompt)
print_instructions(prompt, response)