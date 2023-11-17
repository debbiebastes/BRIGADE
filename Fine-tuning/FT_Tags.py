#import modules needed for Chat GPT comms
import os
import time
import json
import csv
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI()

#model="ft:gpt-3.5-turbo-1106:personal::8KMcfHLQ"
#model="gpt-3.5-turbo-1106"
#model="gpt-4-1106-preview"


def call_ai(prompt, model="ft:gpt-3.5-turbo-1106:personal::8KMcfHLQ"):
    system_message = """
    Given an article text delimited with triple back-ticks, analyze the article and identify three tags that best summarize its main topics. These tags should reflect the key technologies, concepts, and themes covered in the article. 

    Adhere to these steps for consistency and accuracy:
    - If the article mentions several technologies or themes, focus on those that are central to the main argument or purpose of the article.
    - If a technology or theme is mentioned in multiple significant contexts, it should be considered more relevant.
    - Avoid selecting tags that are only briefly mentioned or not central to the article's main points. 
    - Only choose from the list of possible tags provided below:
    LIST OF POSSIBLE TAGS:
    Serverless, Landing Zone, RDS, DynamoDB, Lambda, Control Tower, Multi-AZ, Read Replica, Disaster Recovery, Data Modeling, Performance, Scalability, Cost Optimization, Security, Governance, Observability, Monitoring, DevOps, Machine Learning, Artificial Intelligence, Software Development
    OUTPUT FORMAT:
    - LIST OF TAGS: List the 3 most relevant tags in a simple JSON array.
    """

    messages = [{"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
    ]
    temperature=0.7
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

# def save_to_file(data, filename):
#     #get timestamp in '%Y-%m-%d %H:%M:%S' format
#     timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
#     print('Saving logs to file...',filename)
#     print('timestamp:',timestamp)

#     directory = 'GenAI_exp_logs'
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     with open(f"{directory}/GenAI_FT_{filename}.txt", 'a') as f:
#         f.write("SAVING GENERATED RESPONSE TO FILE " + timestamp + '\n')
#         for key, value in data.items():
#             # If the value is another dictionary (like 'context'), iterate through it separately
#             if isinstance(value, dict):
#                 f.write(f'{key}:\n')
#                 for sub_key, sub_value in value.items():
#                     f.write(f'  {sub_key}: {sub_value}\n')
#             else:
#                 f.write('\n')
#                 f.write(f'{key}: {value}\n')
#         # Add an extra newline for separation between entries
#         f.write('\n')

#test code to get a response from the openai api
article_text =""" """

#read article text from file
with open('./data/article_text.txt', 'r') as f:
    article_text = f.read()
    article_text = article_text.replace('\n', ' ')
    article_text = article_text.replace('\r', '')
    article_text = article_text.replace('\t', '')
    article_text = article_text.strip()


prompt = f"""
Analyze the article and identify three tags that best summarize its main topics
ARTICLE TEXT:
```
{article_text}
```
""" 

#print('Prompt: %s' %prompt)
response = call_ai(prompt)
print(response['body'])
save_to_csv(response,"output_TAGS")