#!/usr/bin/env python3

from JsonOperate.task.get_json_info import get_object_path, get_key_path
from JsonOperate.task.copy_key_value import copy_value
from JsonOperate.task.remove_key_value import remove_value

def move_key_value_task(command, json_data):
    key = command['key']
    source_key_paths = []
    target_key_paths = []
    if 'decorate_source' in command.keys():
        source_key_paths = get_object_path(key, command['decorate_source'], json_data, 'source')
    else:
        key_paths = get_key_path(key, json_data, None, [], {})
        source_key_paths = key_paths[key]
    if 'decorate_target' in command.keys():
        target_key_paths = get_object_path(key, command['decorate_target'], json_data, 'target')
    else:
        key_paths = get_key_path(key, json_data, None, [], {})
        target_key_paths = key_paths[key]
    print(f"source_key_path is {source_key_paths}, target_key_path is {target_key_paths}")
    json_data = copy_value(json_data, source_key_paths, target_key_paths)
    json_data = remove_value(json_data, source_key_paths)
    return json_data
