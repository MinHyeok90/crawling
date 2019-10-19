import os
import json


def get_env():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, '_conf/settings/current_env_mode.json'), 'rt', encoding='UTF-8-sig') as json_file:
        env = json.load(json_file)
    return env