import ahocorasick
import pickle
from main import Rule

# Building the Aho-Corasick automaton
def build_aho_corasick_automaton(rules):
    automaton = ahocorasick.Automaton()
    for rule in rules:
        for pattern in rule.patterns:
            automaton.add_word(pattern, (rule.id, rule.description))
    automaton.make_automaton()
    return automaton

# Searching logs using the Aho-Corasick automaton
def search_logs(automaton, logs):
    matches = []
    for log in logs:
        for end_index, (rule_id, description) in automaton.iter(log):
            matches.append((rule_id, description, log))
    return matches


# Assume `automaton` is the automaton you've built
def save_automaton(automaton, filename='automaton.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(automaton, f)
    print(f"Automaton saved to {filename}")
    
def load_automaton(filename='automaton.pkl'):
    with open(filename, 'rb') as f:
        automaton = pickle.load(f)
    print(f"Automaton loaded from {filename}")
    return automaton


# Example Usage
rules = [
    Rule(1, 3, "SSH login attempt", "Authentication", patterns=["failed password", "Invalid user"]),
    Rule(2, 5, "SQL Injection Attempt", "Database", patterns=["SELECT.*FROM.*WHERE", "UNION SELECT"]),
]

# Building the automaton
automaton = build_aho_corasick_automaton(rules)

# Example logs
logs = [
    "Invalid user admin from 192.168.1.100",
    "User login failed due to invalid password",
    "UNION SELECT username, password FROM users WHERE '1'='1'",
]

# Searching for matches
matches = search_logs(automaton, logs)
for match in matches:
    print(f"Match found: Rule ID {match[0]}, Description: {match[1]}, Log: {match[2]}")
    
save_automaton(automaton)
