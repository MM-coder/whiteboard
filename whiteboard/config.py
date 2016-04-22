# -*- coding: utf-8 -*-
"""User configuration handling"""
import json
import os
import sys

CONFIG_FILENAME = '.whiteboardrc'
GLOBAL_CONFIG_PATH = os.path.join(os.path.expanduser('~'), CONFIG_FILENAME)
DEFAULT_CONFIG = {
    'SECRET_KEY': 'bMYruZ0WbDsJeZI7K6SSZRDgNKCaKsGi',
    'BINDINGS': [],
}


def _from_file(filename):
    def err_and_exit(msg):
        sys.stderr.write(filename + ': ' + msg + '\n')
        sys.exit(1)

    data = {}

    try:
        with open(filename) as f:
            data = json.load(f)
            if not isinstance(data, dict):
                err_and_exit('Expecting config to be dict, got %s'
                             % type(data).__name__)
    except IOError:
        pass
    except json.JSONDecodeError as e:
        err_and_exit(str(e))

    return data


def load_config(path):
    """Load the config file."""
    config = DEFAULT_CONFIG.copy()
    config.update(_from_file(GLOBAL_CONFIG_PATH))
    config.update(_from_file(os.path.join(path, CONFIG_FILENAME)))
    return config
