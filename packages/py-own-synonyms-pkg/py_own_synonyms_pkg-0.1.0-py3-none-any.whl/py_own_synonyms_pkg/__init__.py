import json
import os

# Path to synonyms.json file
synonyms_file_path = os.path.join(os.path.dirname(__file__), 'synonyms.json')

def get_synonyms():
    with open(synonyms_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data