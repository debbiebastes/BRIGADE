import csv
import json

def convert_csv_to_jsonl(csv_file_path, jsonl_file_path):
    """
    Convert a CSV file with columns 'role' and 'content' (case insensitive) to a JSON Lines format.

    Parameters:
    csv_file_path (str): Path to the input CSV file.
    jsonl_file_path (str): Path to the output JSON Lines file.
    """
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file, \
         open(jsonl_file_path, mode='w', encoding='utf-8') as jsonl_file:

        reader = csv.DictReader(csv_file)
        current_conversation = []

        for row in reader:
            # Each new conversation is identified by a new 'system' role message
            if row['role'].lower() == 'system':
                if current_conversation:
                    # Write the previous conversation to the file
                    json.dump({"messages": current_conversation}, jsonl_file)
                    jsonl_file.write('\n')
                    current_conversation = []

            # Append the message to the current conversation
            current_conversation.append({"role": row['role'], "content": row['content']})

        # Write the last conversation if exists
        if current_conversation:
            json.dump({"messages": current_conversation}, jsonl_file)

# Usage example:
csv_file_path = 'data/training_data.csv'
jsonl_file_path = 'FT_data/openai_training_data.jsonl'
convert_csv_to_jsonl(csv_file_path, jsonl_file_path)
