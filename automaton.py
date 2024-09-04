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
def search_logs(automaton, log):
    matches = []
    for end_index, rule in automaton.iter(log):
        matches.append((rule, log))
    return matches