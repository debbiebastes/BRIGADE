import json
from typing import Dict, List

#AWS SDK for Python
import boto3
from botocore.config import Config

#Region of our inference endpoint
my_config = Config(region_name = 'us-east-2') 

#The endpoint name given by our JumpStart deployment
endpoint_name = "jumpstart-dft-hf-llm-mistral-7b-instruct" 

# Call the Generative AI endpoint
def call_ai(prompt):
    instructions = [{"role": "user", "content": prompt}]
    prompt = format_instructions(instructions)
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256, "do_sample": True}
    }
    response = query_endpoint(payload)
    return response

# Helper function: sending the query to the endpoint
def query_endpoint(payload):
    client = boto3.client("runtime.sagemaker", config=my_config)
    response = client.invoke_endpoint(
        EndpointName=endpoint_name, 
        ContentType="application/json", 
        Body=json.dumps(payload).encode("utf-8")
    )
    model_predictions = json.loads(response['Body'].read())
    generated_text = model_predictions[0]['generated_text']
    return generated_text

# Helper function: Mistral-specific prompt formatting
def format_instructions(instructions: List[Dict[str, str]]) -> List[str]:
    """Format instructions where conversation roles must alternate user/assistant/user/assistant/..."""
    prompt: List[str] = []
    for user, answer in zip(instructions[::2], instructions[1::2]):
        prompt.extend(["<s>", "[INST] ", (user["content"]).strip(), " [/INST] ", (answer["content"]).strip(), "</s>"])
    prompt.extend(["<s>", "[INST] ", (instructions[-1]["content"]).strip(), " [/INST] "])
    return "".join(prompt)

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