#!/usr/bin/env python3
from JsonOperate.task.get_json_info import check_key_path, get_object_path, get_key_path
from copy import deepcopy
# import os
import json


def copy_key_value_task(command, json_data):
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
    return json_data


def copy_value(json_data, source_key_paths, target_key_paths):
    len_source = len(source_key_paths)
    len_target = len(target_key_paths)
    if len_source == len_target or len_source == 1:
        values = get_source_value(json_data, source_key_paths)
    else:
        print(f"command error len source is {len_source} len target is {len_target} source path is {source_key_paths}  target path is {target_key_paths} ")
        return json_data

    json_data = assign_value(json_data, source_key_paths, target_key_paths, values)
    
    return json_data

def get_source_value(json_data, source_key_paths):
    # print(f"source path is {source_key_paths}")
    source_data = []
    loop_data = deepcopy(json_data)
    for source_key_path in source_key_paths:
        data = loop_data
        if check_key_path(source_key_path, data):
            for key in source_key_path:
                data = data[key]
            source_data.append(data)
        else:
            print(f"have error key path please check it {source_key_path}")
            return []
    return source_data

def check_copy_condition(source_key_paths, target_key_paths, values):
    len_value = len(values)
    len_target = len(target_key_paths)
    len_source = len(source_key_paths)

    key_paths = target_key_paths
    # here is from one copy to many
    if len_value == 1 and len_target > 1:
        values = [deepcopy(values[0]) for id in range(len_target)]

    len_value = len(values)
    len_key_path = len(key_paths)
    if len_value != len_key_path:
        print(f"copy condition error, please check your command len source path is {len_source}, \
         len target path is {len_target}  len values is {len_value} len key path is {len_key_path}")
        return [], []
    else:
        return key_paths, values

COMPLEX_CASE_NAME = 'HipTD_THOR_56_CAP6_FDD_32x4RX_10MHz_COMP_1.json'
SIMPLE_CASE_NAME = 'HipTD_thor_valid_srs_tdd_bwv_CB008322_G_frCfg1208_td_jumping_trigger_snapshot_1.json'

def assign_value(json_data, source_key_paths, target_key_paths, values):

    key_paths, values = check_copy_condition(source_key_paths, target_key_paths, values)
    
    for key_path, value in zip(key_paths, values):
        if check_key_path(key_path[:-1], json_data):
            data = json_data
            for key in key_path[:-1]:
                data = data[key]

            if isinstance(data, list) and isinstance(key_path[-1], int):
                if len(data) > key_path[-1]:
                    data[key_path[-1]] = value
                else:
                    data.append(value)
            elif isinstance(data, dict) and  isinstance(key_path[-1], str) and key_path[-1] in data.keys():
                data[key_path[-1]] = value
            else:
                print(f"have error key path for add new value please check it {key_path}")
        else:
            print(f"have error key path please check it {key_path}")
            #response invalid key path

    # current_path = os.getcwd()
    # json_path = os.path.join(current_path, "tests", COMPLEX_CASE_NAME)
    # # output_filename = "updated_data.json"
    # with open(json_path, 'w') as outfile:
    #     json.dump(json_data, outfile, indent=4)
    return json_data
    
