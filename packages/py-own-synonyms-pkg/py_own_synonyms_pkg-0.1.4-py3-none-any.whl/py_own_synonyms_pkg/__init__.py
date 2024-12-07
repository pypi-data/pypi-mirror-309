import json
import os

# Path to synonyms.json file inside the package directory
synonyms_file_path = os.path.join(os.path.dirname(__file__), 'py_own_synonyms_pkg', 'synonyms.json')

def get_synonyms():
    # Read and load the synonyms data from the JSON file
    with open(synonyms_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
