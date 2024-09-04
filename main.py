import os
from dataFormatter import save_file,load_file,append_rules_to_json
from rules import parse_ossec_rules
from constants import rules_directory, rules_data_file,data_directory
from constants import parsed_rules_json_file,automaton_data_file
from automaton import build_automaton
from fileMonitor import LogMonitor

if __name__ == '__main__':
    # create data directory if it does not exist
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
        
    # create rules pickle data file if it does not exist
    if not os.path.exists(rules_data_file):
        parsed_all_rules = parse_ossec_rules(rules_directory)
        save_file(parsed_all_rules,rules_data_file)
    else:
        parsed_all_rules = load_file(rules_data_file)
    
    # create parsed rules json file if it does not exist
    if not os.path.exists(parsed_rules_json_file):
        append_rules_to_json(parsed_rules_json_file,parsed_all_rules)
    
    # create automaton pickle data file if it does not exist
    if not os.path.exists(automaton_data_file):
        automaton = build_automaton(parsed_all_rules)
        save_file(automaton,automaton_data_file)
    else:
        automaton = load_file(automaton_data_file)
        
    # create log monitor
    monitor = LogMonitor()
    
    # run log monitor to keep track of changes in monitoring files
    monitor.run()
    
    # # Example Usage
    # rules = [
    #     Rule(1, 3, "SSH login attempt", "Authentication", patterns=["failed password", "Invalid user"]),
    #     Rule(2, 5, "SQL Injection Attempt", "Database", patterns=["SELECT.*FROM.*WHERE", "UNION SELECT"]),
    # ]

    # # Building the automaton
    # automaton = build_aho_corasick_automaton(rules)

    # # Example logs
    # logs = [
    #     "Invalid user admin from 192.168.1.100",
    #     "User login failed due to invalid password",
    #     "UNION SELECT username, password FROM users WHERE '1'='1'",
    # ]

    # # Searching for matches
    # matches = search_logs(automaton, logs)
    # for match in matches:
    #     print(f"Match found: Rule ID {match[0]}, Description: {match[1]}, Log: {match[2]}")        
    