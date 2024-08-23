from main import is_attack_detected,all_rules

tests = [
    "Failed opening the log files please check the permissions"
]
for sample_log in tests:
    attack_detected, matching_rule = is_attack_detected(sample_log, all_rules)
    if attack_detected:
        print(matching_rule,sample_log)
        print(f"Attack detected! Rule ID: {matching_rule.id}, Description: {matching_rule.description}, Level: {matching_rule.level}, Category: {matching_rule.category}")
    else:
        print("No attack detected.")