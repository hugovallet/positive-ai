from typing import Dict

import yaml


def read_yaml(config_file_path: str) -> Dict:
    with open(config_file_path) as stream:
        try:
            loaded = yaml.safe_load(stream)
            return loaded
        except yaml.YAMLError as exc:
            raise exc
