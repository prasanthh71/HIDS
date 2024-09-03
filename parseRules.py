from main import parse_ossec_rules
from constants import rules_directory, parsed_rules_file
import json

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

if __name__ == '__main__':
    all_rules = parse_ossec_rules(rules_directory)
    append_rules_to_json(parsed_rules_file,all_rules)