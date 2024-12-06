#!/usr/bin/env python3

from JsonOperate.task.get_json_info import check_key_path, get_object_path, get_key_path
from JsonOperate.task.add_key_value import interpret_value

def value_change_task(command, json_data):
    key = command['key']
    value = command['value']
    target_key_paths = []

    if 'decorate_target' in command.keys():
        target_key_paths = get_object_path(key, command['decorate_target'], json_data, 'target')
    else:
        key_paths = get_key_path(key, json_data, None, [], {})
        target_key_paths = key_paths[key]

    print(f"target_key_path is {target_key_paths}")
    json_data = change_value(json_data, value, target_key_paths)
    return json_data

def change_value(json_data, value, key_paths):
    for key_path in key_paths:
        if check_key_path(key_path[:-1], json_data):
            data = json_data
            for sub_key in key_path[:-1]:
                # print(f"subkey_is {sub_key}")
                data = data[sub_key]
            # print(f"key_is {key} value is {value} data is {data}")

            # data[key_path[-1]] = interpret_value(value)
            data[key_path[-1]] = value
        else:
            print(f"have error key path please check it {key_path}")
    return json_data