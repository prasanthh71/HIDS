import re
from collections import defaultdict

def build_automaton(rules):
    # automaton = ahocorasick.Automaton()
    # for rule in rules:
    #     for pattern in rule.patterns:
    #         automaton.add_word(pattern, rule)
    # automaton.make_automaton()
    automata = defaultdict(list)
    for rule in rules:
        for pattern in rule.patterns:
            try:
                words = re.findall(r'\b\w+\b', pattern)
                if not words:
                    first_char = next((c for c in pattern if c not in '^\\S+[]'), '')
                    automata[first_char].append((re.compile(pattern), rule))
                else:
                    for word in words:
                        automata[word].append((re.compile(pattern), rule))
            except re.error as e:
                print(f"Error in rule {rule.id}, pattern '{pattern}': {str(e)}")
                continue
    return automata

# Searching logs using the Aho-Corasick automaton
def search_logs(automaton, log):
    matched_rules = set()
    words = set(re.findall(r'\b\w+\b', log))
    
    for word in words:
        if word in automaton:
            for pattern,rule in automaton[word]:
                if pattern.search(log):
                    matched_rules.add(rule)
    return list(matched_rules)