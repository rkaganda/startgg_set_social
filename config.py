# config.py
import yaml
import os

# Dictionary to store the current configuration
current_config = {}


def load_config_from_file(filename):
    global current_config
    with open(filename, 'r') as file:
        current_config = yaml.safe_load(file)


def save_config_to_file(filename):
    global current_config
    with open(filename, 'w') as file:
        yaml.safe_dump(current_config, file)


# Check if 'test_config.yaml' exists when the module is loaded for the first time
config_filename = 'test_config.yaml'
if os.path.exists(config_filename):
    load_config_from_file(config_filename)
