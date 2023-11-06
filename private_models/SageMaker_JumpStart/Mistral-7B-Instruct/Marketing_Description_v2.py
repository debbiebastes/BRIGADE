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
response = call_ai(prompt)
print_instructions(prompt, response)