#import modules needed for Chat GPT comms
import os
import time
import json
import csv
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI()

#model="ft:gpt-3.5-turbo-1106:personal::8LPZfKpe"
#model="gpt-3.5-turbo-1106"
#model="gpt-4-1106-preview"


def call_ai(prompt, model="gpt-3.5-turbo-1106"):
    # system_message = """
    # "Your task is to identify the sentiment of a product review.
    # """

    # messages = [{"role": "system", "content": system_message},
    #             {"role": "user", "content": prompt}
    # ]

    messages = [
        {"role": "user", "content": prompt}
    ]
    temperature=0.5
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return {
        'body': response.choices[0].message.content,
        'context': {
            'ChatGPT model': response.model,
            'temperature': temperature,
            'ChatGPT token usage': response.usage,
            'prompt': prompt,
        }
    }
def save_to_csv(data, filename):
    # Get timestamp in '%Y-%m-%d %H:%M:%S' format
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print('Saving logs to file...', filename)
    print('timestamp:', timestamp)

    directory = 'GenAI_exp_logs'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"{directory}/GenAI_FT_{filename}.csv"

    # Function to flatten the dictionary
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    # Flatten the data dictionary
    flat_data = flatten_dict(data)

    # Include timestamp in the flattened data
    flat_data['timestamp'] = timestamp

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=flat_data.keys())

        # Write headers only if the file is empty/new
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(flat_data)

#test code to get a response from the openai api
review_text =""" """

#read article text from file
with open('./data/review.txt', 'r') as f:
    review_text = f.read()


prompt = f"""
Here is a product review from a customer, which is delimited with triple backticks.
{review_text}

    What is the sentiment of that product review?
    Identify the product being reviewed.
    Enumerate the positive and negative aspects of the product review.
    The response should be in JSON format  with the following elements:
            - Product name
            - Review Sentiment (Positive/Negative/Neutral)
            - Positive comments about the product (Enumerate)
            - Negative comments about the product (Enumerate)

Answer:
""" 

print('Prompt: %s' %prompt)
response = call_ai(prompt)
print(response['body'])
save_to_csv(response,"output_SENTI")