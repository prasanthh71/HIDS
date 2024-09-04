import pickle
import json

def save_file(object, filename):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(object, f)
    except Exception as e:
        print(f"Error saving object:{object} to file:{filename}: {str(e)}")
    
def load_file(filename):
    try:
        with open(filename, 'rb') as f:
            object = pickle.load(f)
        return object
    except Exception as e:
        print(f"Error loading object from file:{filename}")
        

def append_rules_to_json(file_path, list_of_rules):
    rules_data = [rule.to_dict() for rule in list_of_rules]
    
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.extend(rules_data)
    
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)