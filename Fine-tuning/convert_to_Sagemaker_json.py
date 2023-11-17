import pandas as pd
import json

def convert_csv_to_jsonl(csv_file_path, jsonl_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Filter rows based on the 'role' and reset index for proper pairing
    user_rows = df[df['role'] == 'user'].reset_index(drop=True)
    assistant_rows = df[df['role'] == 'assistant'].reset_index(drop=True)

    # Check if each user message has a corresponding assistant message
    if len(user_rows) != len(assistant_rows):
        raise ValueError("Mismatch in the number of user and assistant messages.")

    # Pair user and assistant messages
    paired_messages = [{"question": user, "answer": assistant} 
                       for user, assistant in zip(user_rows['content'], assistant_rows['content'])]

    # Convert to JSON Lines format and write to a file
    with open(jsonl_file_path, 'w') as file:
        for record in paired_messages:
            file.write(json.dumps(record) + '\n')

# Example usage
csv_file_path = './data/senti_training_dataset.csv'
jsonl_file_path = './Sagemaker/train/senti_training_dataset.jsonl'
convert_csv_to_jsonl(csv_file_path, jsonl_file_path)
