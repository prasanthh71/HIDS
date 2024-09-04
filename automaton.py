import ahocorasick

# Building the Aho-Corasick automaton
def build_automaton(rules):
    automaton = ahocorasick.Automaton()
    for rule in rules:
        for pattern in rule.patterns:
            automaton.add_word(pattern, rule)
    automaton.make_automaton()
    return automaton

# Searching logs using the Aho-Corasick automaton
def search_logs(automaton, logs):
    matches = []
    for log in logs:
        for end_index, rule in automaton.iter(log):
            matches.append((rule.id, rule.description, log))
    return matches