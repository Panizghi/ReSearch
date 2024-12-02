# %% [markdown]
# # Semantic Search Test

# %% [markdown]
# ## Install Requirements

# %%
!pip install requests

# %%
!pip install elasticsearch

# %% [markdown]
# ## Invoke ES Client

# %%
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

# %% [markdown]
# ## Load Env

# %%
load_dotenv()

# %% [markdown]
# # Verify Defaults

# %%
url = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
username: str = os.getenv('ELASTICSEARCH_USERNAME', 'elastic')
password: str = os.getenv('ELASTICSEARCH_PASSWORD', '')
ca_certs_path = os.getenv('ELASTICSEARCH_CA_CERTS')
es_index_name: str = os.getenv('ELASTICSEARCH_INDEX_NAME', 'default_index')
timeout: int = int(os.getenv('ELASTICSEARCH_TIMEOUT', '30'))

es_client = Elasticsearch(url,
            basic_auth=(username, password),
            ca_certs=ca_certs_path,
            timeout=timeout,
            verify_certs=True
        )

# %% [markdown]
# ## Print ENV

# %%
print("Elasticsearch URL:", url)
print("Elasticsearch Username:", username)
print("Elasticsearch Password:", password)
print("Elasticsearch CA Certs Path:", ca_certs_path)
print("Elasticsearch Index Name:", es_index_name)
print("Elasticsearch Timeout:", timeout)

# %%
print(es_client.info())

# %% [markdown]
# ## Ping ES

# %%
print(es_client.info())

# %% [markdown]
# ## Test OpenAI

# %%
from openai import OpenAI

openai_client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("aiCUSTOM_ENV_NAME"),
# )


completion = openai_client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)

# %% [markdown]
# # Generate Query Embeddings

# %%
text = "What is the size of the plasma-derived market, and at what rate is it expanding?" 
clean_text = text.replace("\n", " ").strip()

response = openai_client.embeddings.create(input=[clean_text], model="text-embedding-3-small")
query_vector = response.data[0].embedding
print(query_vector) if response else None

# %% [markdown]
# # ES KNN Search using the Query Vector

# %%
# Context Embedding vs Question Embedding
k = 3
all_hits = []
tags = None
tags_query = {"terms": {"tag": tags}} if tags else {}
response_context = es_client.search(
                index=es_index_name,
                knn={
                    "field": "context_embedding",
                    "query_vector": query_vector,
                    "k": k,
                    "num_candidates": 100
                },
                _source=["context", "expert_answer", "original_question", "filename", "subject", "event_id",
                         "document_id"]
            )
# response_question = es_client.search(
#                 index=es_index_name,
#                 knn={
#                     "field": "question_embedding",
#                     "query_vector": query_vector,
#                     "k": k,
#                     "num_candidates": 100,
#                     "filter": {
#                         "has_child": {
#                             "type": "tags_as_childs",
#                             "query": {
#                                 "bool": {
#                                     "must": [tags_query] if tags_query else []
#                                 }
#                             },
#                             "score_mode": "none"
#                         }
#                     }
#                 },
#                 _source=["analyst_question", "expert_answer", "original_question", "filename", "subject", "event_id",
#                          "document_id"]
#             )
print(response)
response = response_context

if response and response['hits']['hits']:
    all_hits.extend(response['hits']['hits'])

print(all_hits)

# %% [markdown]
# # Aggregate Overall Score

# %%
score_aggregation = {}
hits = all_hits
for hit in hits:
    event_id = hit['_source']['event_id']
    doc_id = hit['_source']['document_id']
    subject = hit['_source']['subject']
    filename = hit['_source']['filename']
    combination_key = f"{event_id}-{doc_id}"

    if combination_key not in score_aggregation:
        score_aggregation[combination_key] = {
            'total_score': 0.0,  # Keep as float during aggregation
            'hits': 0,
            'details': [],
            'document_id': doc_id,
            'event_id': event_id,
            'subject': subject,
            'filename': filename
        }
            
    score_aggregation[combination_key]['total_score'] += float(hit['_score'])
    score_aggregation[combination_key]['hits'] += 1
    detail = {
        'context': hit['_source']['context'],
        'original_question': hit['_source']['original_question'],
        'expert_answer': hit['_source']['expert_answer'],
        'similarity_score': f"{float(hit['_score']) * 100:.2f}%",
    }
    score_aggregation[combination_key]['details'].append(detail)

# After all hits are processed, calculate and format total_score as a percentage
for key, value in score_aggregation.items():
    if value['hits'] > 0:
        value['total_score'] = f"{(value['total_score'] / value['hits']) * 100:.2f}%"
    else:
        value['total_score'] = "0.00%"

print(score_aggregation)
documents = score_aggregation

results = [value for key, value in documents.items()]

print(len(results))
print(results)


# %%


# %% [markdown]
# ## Call Semantic Search

# %%
import requests
import json

# API endpoint URL
url = 'http://localhost:8000/v0/search'

# Headers for the request
headers = {
    'Content-Type': 'application/json'
}


data = {
    "questions": ["What is Bipolar Depression?"],
    "tags": [],
    "k": 5,
}

# Convert the data dictionary to JSON
data_json = json.dumps(data)

# Send POST request
response = requests.post(url, headers=headers, data=data_json)

# Print response
print("Status Code:", response.status_code)
print("Response Body:")
print(response.json())

# %%
from jinja2 import Environment, BaseLoader

class TemplateMaker:
    def __init__(self, template_string):
        self.template_string = template_string
        self.template = Environment(loader=BaseLoader).from_string(self.template_string)

    def render(self, **kwargs):
        return self.template.render(**kwargs)
    
    def add_context(self, context):
        return context

    def add_tags(self, tags):
        return ', '.join(tags)

    def add_follow_up_question(self, question):
        return question

    def create_prompt(self, role, content):
        return {
            "role": role,
            "content": content
        }

    def create_message(self, role, context, question, description=None, tags=None, follow_up_question=None):
        message = self.render(role=role, description=description, context=context, question=question)
        if tags:
            message += "\nTags: " + self.add_tags(tags)
        if follow_up_question:
            message += "\nFollow-up question: " + self.add_follow_up_question(follow_up_question)
        return message
    

    import json
import jsonschema
from jsonschema import validate

class MessageValidator:
    def __init__(self, schema_files):
        self.schemas = {}
        for schema_name, file_path in schema_files.items():
            with open(file_path, 'r') as f:
                self.schemas[schema_name] = json.load(f)

    def validate_message(self, message, schema_name):
        schema = self.schemas.get(schema_name)
        if not schema:
            return False, f"Schema '{schema_name}' not found"
        try:
            validate(instance=message, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            return False, err.message
        return True, "Validation successful"

schema_files = {
    "template1": "Templates/Schemas/schema_1.json",
    "template2": "Templates/Schemas/schema_2.json",
    "template3": "Templates/Schemas/schema_3.json",
    "template4": "Templates/Schemas/schema_4.json"
}

message_validator = MessageValidator(schema_files)




# %% [markdown]
# ## LLM Filtering

# %%
import requests
import json
import openai
from typing import List, Optional, Dict

class OpenAIService:
    def __init__(self):
        # Initialize the OpenAI client properly
        # Replace with your actual OpenAI API key
        self.client = OpenAI()

    def get_all_answers(self, results: List[Dict]) -> List[str]:
        """
        Extracts all the expert answers from search results.

        Args:
            results (List[Dict]): List containing the 'details' key with sub-dictionaries of potential answers.

        Returns:
            List[str]: A list containing all extracted expert answers.
        """
        details = results[0].get('details', [])
        all_answers = [
            detail.get('expert_answer', 'No answer provided') for detail in details
        ]
        return all_answers

    def get_best_answer(self, question: str, answers: List[str]) -> Optional[str]:
        """
        Uses OpenAI API to identify the best answer from a list of answers.

        Args:
            question (str): The original question being asked.
            answers (List[str]): List of potential answers to evaluate.

        Returns:
            Optional[str]: The best answer as selected by the OpenAI API, or None if an error occurred.
        """
        # Set up the conversation prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant trained to select the most relevant answer to a given question from a list of possible answers.If none of the possible "},
            {"role": "user", "content": question}
        ]

        # Add each answer to the prompt with its corresponding index
        for idx, answer in enumerate(answers, 1):
            messages.append({"role": "user", "content": f"Answer {idx}: {answer}"})

        # Ask the assistant to determine which answer is the most relevant
        messages.append({"role": "user", "content": "Which answer is the most relevant?"})

        # Query the OpenAI API
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                temperature=0
            )

            # Extract the index of the best answer from the assistant's response
            best_answer_text = response.choices[0].message.content
            best_answer_index = int(''.join(filter(str.isdigit, best_answer_text)))

            # Ensure the index is within the correct range
            if 1 <= best_answer_index <= len(answers):
                return answers[best_answer_index - 1]
            else:
                print(f"Invalid best answer index returned: {best_answer_index}")
                return None

        except Exception as e:
            print(f"An error occurred while selecting the best answer: {e}")
            return None

if response.status_code == 200:
    response_data = response.json()
    results = response_data['results']
    print(results)
    # Extract all answers
    openai_manager = OpenAIService()
    all_answers = openai_manager.get_all_answers(results)
    print("Extracted Answers:")
    for idx, answer in enumerate(all_answers, 1):
        print(f"{idx}. {answer}")

    # Retrieve the best answer using OpenAI
    best_answer = openai_manager.get_best_answer("What is life?", all_answers)
    if best_answer:
        print("\nBest Answer:")
        print(best_answer)
    else:
        print("\nNo valid best answer found.")
else:
    print("Failed to get a valid response from the semantic search API")

# %%
# save the question into a file  and save the asnwer separately 
def save_question_answer(question, answer):
    with open("question.txt", "w") as question_file:
        question_file.write(question)
    with open("answer.txt", "w") as answer_file:
        answer_file.write(answer)

# %%



