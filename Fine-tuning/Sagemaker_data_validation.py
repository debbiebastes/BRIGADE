import json
import tiktoken # for token counting
import numpy as np
from collections import defaultdict

# Replace with the actual path to your dataset
data_path = "./Sagemaker/train/senti_training_dataset.jsonl"

# Load the dataset
with open(data_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]

# Initial dataset stats
print("Num examples:", len(dataset))
print("First example:", dataset[0])

# Format error checks
format_errors = defaultdict(int)

for ex in dataset:
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue

    if "question" not in ex or not isinstance(ex["question"], str):
        format_errors["missing_or_invalid_prompt"] += 1

    if "answer" not in ex or not isinstance(ex["answer"], str):
        format_errors["missing_or_invalid_completion"] += 1

# Report format errors
if format_errors:
    print("Found errors:")
    for k, v in format_errors.items():
        print(f"{k}: {v}")
else:
    print("No errors found")

# Token Counting and Statistical Analysis
encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(encoding.encode(text))

prompt_lengths = []
completion_lengths = []

for ex in dataset:
    prompt_lengths.append(count_tokens(ex["question"]))
    completion_lengths.append(count_tokens(ex["answer"]))

def print_distribution(values, name):
    print(f"\n#### Distribution of {name}:")
    print(f"min / max: {min(values)}, {max(values)}")
    print(f"mean / median: {np.mean(values)}, {np.median(values)}")
    print(f"p5 / p95: {np.quantile(values, 0.05)}, {np.quantile(values, 0.95)}")

print_distribution(prompt_lengths, "Prompt Token Lengths")
print_distribution(completion_lengths, "Completion Token Lengths")
