#import modules needed for Chat GPT comms
import GenAI_faker
import os
import csv


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

GenAI_faker.api_key  = os.getenv('OPENAI_API_KEY')

def parse_file_to_dictionary():
    with open('test_data/product_catalog.csv', 'r') as f:
        reader = csv.DictReader(f)
        data_dict = [row for row in reader]
        return data_dict

product_catalog = parse_file_to_dictionary()

#create product review for each product in the catalog
for product in product_catalog:
    print("Product: \n", product)
    product_review = GenAI_faker.product_review(product)
    print("Product Review: \n", product_review)