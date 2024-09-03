# import re
# from typing import List, Dict, Any
# from main import Rule

# class TrieNode:
#     def __init__(self):
#         self.children: Dict[str, TrieNode] = {}
#         self.rules: List[Rule] = []
#         self.is_end = False

# class Trie:
#     def __init__(self):
#         self.root = TrieNode()

#     def insert(self, pattern: str, rule: 'Rule'):
#         node = self.root
#         for char in pattern:
#             if char not in node.children:
#                 node.children[char] = TrieNode()
#             node = node.children[char]
#         node.is_end = True
#         node.rules.append(rule)

#     def search(self, text: str) -> List['Rule']:
#         matched_rules = []
#         n = len(text)

#         for i in range(n):
#             node = self.root
#             for j in range(i, n):
#                 if text[j] not in node.children:
#                     break
#                 node = node.children[text[j]]
#                 if node.is_end:
#                     matched_rules.extend(node.rules)

#         return matched_rules

# class RuleMatcher:
#     def __init__(self, rules: List[Rule]):
#         self.trie = Trie()
#         for rule in rules:
#             for pattern in rule.patterns:
#                 self.trie.insert(pattern, rule)

#     def match(self, log_entry: str) -> List[Rule]:
#         return self.trie.search(log_entry)

# # Example usage
# rules = [
#     Rule("1", "5", "Successful sudo to ROOT executed", "sudo", ["sudo: session opened for user root"]),
#     Rule("2", "10", "Multiple failed login attempts", "auth", ["Failed password for .* from .* port \d+ ssh2"])
# ]

# matcher = RuleMatcher(rules)

# # Test with a log entry
# log_entry = "May 15 10:20:30 server sudo: session opened for user root by (uid=0)"
# matched_rules = matcher.match(log_entry)

# for rule in matched_rules:
#     print(f"Matched: {rule}")

# # Test with another log entry
# log_entry = "May 15 10:25:45 server sshd[12345]: Failed password for invalid user test from 192.168.1.100 port 22341 ssh2"
# matched_rules = matcher.match(log_entry)

# for rule in matched_rules:
#     print(f"Matched: {rule}") 


# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# import re
# from collections import defaultdict


# class OptimizedHIDS:
#     def __init__(self):
#         self.rules = []
#         self.pattern_index = defaultdict(list)

#     def add_rule(self, rule):
#         self.rules.append(rule)
#         for pattern in rule.patterns:
#             keywords = self._extract_keywords(pattern)
#             print(keywords)
#             for keyword in keywords:
#                 self.pattern_index[keyword].append((rule, pattern))

#     def _extract_keywords(self, pattern):
#         # Extract static parts of the regex pattern as keywords
#         return re.findall(r'\b\w+\b', re.sub(r'[\^\$\.\*\+\?\{\}\[\]\(\)\|\\]', ' ', pattern))

#     def match_log_entry(self, log_entry):
#         matched_rules = set()
#         words = set(re.findall(r'\b\w+\b', log_entry))
#         print(words)
#         for word in words:
#             for rule, pattern in self.pattern_index.get(word, []):
#                 if re.compile(pattern).search(log_entry):
#                     matched_rules.add(rule)

#         return list(matched_rules)

# # Usage example
# hids = OptimizedHIDS()

# # Add rules
# rule1 = Rule("1", "5", "Potential SQL injection", "web_attack", ["SELECT.*FROM", "UNION.*SELECT"])
# rule2 = Rule("2", "3", "Failed login attempt", "authentication", ["Failed login for user .*"])
# rule3 = Rule("30101","0","Apache error messages grouped.","apache",["^\\[error\\]"])
# rule4 = Rule("43","23","error messages grouped.","test",["\\[error\\]"])

# hids.add_rule(rule1)
# hids.add_rule(rule2)
# hids.add_rule(rule3)
# hids.add_rule(rule4)
# print(hids.pattern_index)

# # Test log entries
# log1 = "User attempted SELECT * FROM users UNION SELECT password FROM admin"
# log2 = "Failed login for user admin from IP 192.168.1.100"

# matched_rules3 = hids.match_log_entry("this is [error] From user cbpraveen")


# print("Matched rules for log3:", [str(rule) for rule in matched_rules3])

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

import ahocorasick

class Rule:
    def __init__(self, id, level, description, category, patterns=None):
        self.id = id
        self.level = int(level) if level else 0
        self.description = description
        self.category = category
        self.patterns = patterns or []

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'description': self.description,
            'category': self.category,
            'patterns': self.patterns
        }

    def __str__(self) -> str:
        return f"Rule ID: {self.id}, Description: {self.description}, Level: {self.level}, Category: {self.category}"

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

import pickle

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
