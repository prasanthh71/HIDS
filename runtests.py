import configparser
from main import parse_ossec_rules,rules_directory,is_attack_detected
import os
import logging

def setup_logging(log_file='test_failures.log'):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def parse_test_file(file_path):
    config = configparser.ConfigParser(allow_no_value=True, interpolation=None)
    config.read(file_path)

    tests = []
    for section in config.sections():
        test = {
            'name': section,
            'logs': [],
            'rule': config.get(section, 'rule', fallback=None),
            'alert': config.get(section, 'alert', fallback=None),
            'decoder': config.get(section, 'decoder', fallback=None)
        }
        for key, value in config.items(section):
            if key.startswith('log ') and key.endswith(' pass'):
                test['logs'].append(value)
        tests.append(test)
    return tests

def run_tests(rules, test_directory):
    setup_logging()
    total_tests = 0
    passed_tests = 0

    for filename in os.listdir(test_directory):
        if filename.endswith('.ini'):
            file_path = os.path.join(test_directory, filename)
            try:
                tests = parse_test_file(file_path)
            except Exception as e:
                print(f"Error parsing test file {filename}: {str(e)}")
                continue
            
            for test in tests:
                total_tests += 1
                expected_rule_id = test['rule']
                expected_alert = int(test['alert']) if test['alert'] is not None else None

                for log in test['logs']:
                    is_attack, detected_rule = is_attack_detected(log, rules)
                    
                    if is_attack and detected_rule.id == expected_rule_id:
                        passed_tests += 1
                        break
                    else:
                        log_message = (
                            f"Test failed: {test['name']}, File: {filename}\n"
                            f"Expected rule: {expected_rule_id}, Expected alert: {expected_alert}\n"
                            f"Log: {log}\n"
                        )
                        if is_attack:
                            log_message += (
                                f"Detected rule: {detected_rule.id}, Detected alert level: {detected_rule.level}\n"
                            )
                        else:
                            log_message += "No rule detected\n"
                        
                        logging.info(log_message)

    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Accuracy: {passed_tests / total_tests * 100:.2f}%")
    
if __name__ == "__main__":
    test_directory = './tests'

    rules = parse_ossec_rules(rules_directory)
    run_tests(rules, test_directory)