#!/usr/bin/env python3

from JsonOperate.task.get_json_info import check_key_path, get_object_path, get_key_path
import json

def add_key_value_task(command, json_data):
    key = command['key']
    value = command['value']
    target_key_paths = []

    if 'decorate_target' in command.keys():
        target_key_paths = get_object_path(command['decorate_target'][-1]['target'], command['decorate_target'], json_data, 'target')
    else:
        key_paths = get_key_path(key, json_data, None, [], {})
        target_key_paths = key_paths[key]
    print(f"target_key_path is {target_key_paths}")
    json_data = add_value(json_data, key, value, target_key_paths)
    return json_data


def add_value(json_data, key, value, key_paths):
    for key_path in key_paths:
        # jsonpath_string = "$." + ".".join(str(element) if isinstance(element, int) else element for element in key_path)
        if check_key_path(key_path[:-1], json_data):
            data = json_data
            for sub_key in key_path[:-1]:
                # print(f"subkey_is {sub_key}")
                data = data[sub_key]
            print(f"key_is {key} value is {value} data is {data}")
            if data[key_path[-1]] is None:
                data[key_path[-1]] = {}
            data = data[key_path[-1]]
            if key == key_path[-1]:
                if isinstance(data, list):
                    if isinstance(value, list):
                        data += value
                    else:
                        data.append(value)
                elif isinstance(data, dict):
                    if isinstance(value, dict):
                        data.update(value)
                    else:
                        print(f"couldn't add not dict items into a dict, may be you should use chanage command")
                else:
                    data[key] = value
            else:
                data[key] = value
        else:
            print(f"have error key path please check it {key_path}")
    return json_data

def interpret_value(input_str):
    try:
        value = json.loads(input_str)
        return value
    except json.JSONDecodeError:
        return input_str
