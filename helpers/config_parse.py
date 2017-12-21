#!/usr/bin/env python2
from __future__ import print_function

import json
import os
import shutil


def read_config(config_path):
    with open(config_path, 'r') as f:
        data = json.load(f)
    return data


def write_config(config_dict, config_path):
    with open(config_path, 'w') as f:
        json.dump(config_dict, f)


def read_or_create_config(config_path, default_config, app_name):
    # type: (str, str, str) -> dict
    """
    reads the config in `config_path` if invalid, replaces it with `default_config` and saves the erroneous config
    in `config_path`.failed

    >>> print('{"configtype":"sample", "version":1}', file=open('/tmp/a_valid_config_file',"w"))
    >>> print('{{{zzz', file=open('/tmp/a_invalid_config_file',"w"))
    >>> c = read_or_create_config("/tmp/a_valid_config_file", '{"default_config":True}', "test_runner")
    >>> c['configtype']
    u'sample'

    >>> c = read_or_create_config("/tmp/a_invalid_config_file", '{"default_config":true}', "test_runner")
    test_runner: broken/nonexistent config, restoring with defaults...
    >>> os.path.exists("/tmp/a_invalid_config_file.failed")
    True
    >>> c['default_config']
    True
    """
    try:
        config_dict = read_config(config_path)
    except (ValueError, IOError):
        print("{}: broken/nonexistent config, restoring with defaults...".format(app_name))
        if os.path.exists(config_path):
            shutil.move(config_path, config_path + ".failed")
        with open(config_path, 'w') as f:
            f.write(default_config)
        config_dict = read_config(config_path)
    return config_dict


if __name__ == "__main__":
    config = read_config("../config.json")
    print(config)
