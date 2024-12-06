#!/usr/bin/env python3

from JsonOperate.task.get_json_info import check_key_path, get_object_path, get_key_path

def remove_key_value_task(command, json_data):
    key = command['key']
    target_key_paths = []

    if 'decorate_target' in command.keys():
        target_key_paths = get_object_path(key, command['decorate_target'], json_data, 'target')
    else:
        key_paths = get_key_path(key, json_data, None, [], {})
        target_key_paths = key_paths[key]

    print(f"target_key_paths is {target_key_paths}")
    json_data = remove_value(json_data, target_key_paths)
    return json_data

def remove_value(json_data, key_paths):
    for key_path in reversed(key_paths):
        if check_key_path(key_path[:-1], json_data):
            data = json_data
            for sub_key in key_path[:-1]:
                print(f"subkey_is {sub_key}")
                data = data[sub_key]
            # print(f"data is {data}")
            del data[key_path[-1]]
            print(f"after remove data is {data}")

        else:
            print(f"have error key path please check it {key_path}")
    return json_data