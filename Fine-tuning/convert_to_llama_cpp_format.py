import csv

def convert_csv_to_text(csv_file_path, text_file_path):
    """
    Convert a CSV file with columns 'role' and 'content' (case insensitive) to a text file.
    The text file contains lines each with a concatenated 'user' and 'assistant' content, separated by a newline
    after the 'assistant' response.
    
    Parameters:
    csv_file_path (str): Path to the input CSV file.
    text_file_path (str): Path to the output text file.
    """
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file, \
         open(text_file_path, mode='w', encoding='utf-8') as text_file:

        reader = csv.DictReader(csv_file)
        user_content = None

        for row in reader:
            role = row['role'].lower()
            content = row['content']

            if role == 'user':
                user_content = content
            elif role == 'assistant' and user_content is not None:
                # Concatenate user and assistant content, then write to the text file
                combined_content = '\n<s>\n' + user_content + ' ' + content
                text_file.write(combined_content)
                user_content = None  # Reset user content for the next pair

# Usage example:
csv_file_path = 'data/senti_data.csv'
text_file_path = 'FT_data/llama_cpp_senti_training_datav1116.txt'
convert_csv_to_text(csv_file_path, text_file_path)