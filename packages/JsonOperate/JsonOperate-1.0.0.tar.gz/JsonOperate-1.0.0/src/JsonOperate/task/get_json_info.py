
from collections import defaultdict
from jsonpath_ng import jsonpath, parse
import json
from copy import deepcopy

source_commands = ['source','source_key','source_condition','source_condition_value']
target_commands = ['target','target_key','target_condition','target_condition_value']

def get_key_info_task(command, json_data):
    key = command['key']
    target_key_paths = []

    if 'decorate_target' in command.keys():
        target_key_paths = get_object_path(key, command['decorate_target'], json_data, 'target')
    else:
        key_paths = get_key_path(key, json_data, None, [], {})
        target_key_paths = key_paths[key]

    print(f"target_key_path is {target_key_paths}")
    result_data = add_response_value(json_data, target_key_paths)
    return result_data

def add_response_value(json_data, source_key_paths):
    result_data = []
    loop_data = deepcopy(json_data)
    for source_key_path in source_key_paths:
        data = loop_data
        if check_key_path(source_key_path, data):
            store_key = ''
            for key in source_key_path:
                store_key += f'->{json.dumps(key)}'
                data = data[key]
            value = compress_value(data)
            print(f"value is {value}")
            result_data.append({store_key:value})
        else:
            print(f"have error key path please check it {source_key_path}")
        
    return result_data

def compress_value(data):
    if isinstance(data, list):
        source_data = []
        for subdata in data:
            if isinstance(subdata, dict):
                sub_source_data = []
                for key in subdata.keys():
                    sub_source_data.append(key)
                source_data.append(sub_source_data)
            else:
                source_data.append(subdata)
    elif isinstance(data, dict):
        source_data = []
        for key in data.keys():
            source_data.append(key)
    else:
        source_data = data
    return source_data

def select_right_path(paths, condition_paths):
    return [filter_path for path in paths for filter_path in filter_path_by_condition(path, condition_paths)]

#[[[obj1,1],[obj1,2]],[[obj2,2]],[[obj3]]]
def filter_path_by_condition(path, condition_paths):
    filter_paths = [path]
    for condition_obj_paths in condition_paths:
        for condition_path in condition_obj_paths:
            # if len(condition_path) == 2:
            #     print(f"condition_path is {condition_path}, path is {path}")
            if isinstance(condition_path[-1], int) and condition_path[:-1] == path:
                int_path = path[:]
                int_path.append(condition_path[-1])
                filter_paths.append(int_path)
        filter_paths = collect_condition_path(filter_paths, condition_obj_paths)
        # if filter_paths:
        #     print(f"filter_paths is {filter_paths}, condition_obj_paths is {condition_obj_paths}")
    return filter_paths

def collect_condition_path(filter_paths, condition_obj_paths):
    return [filter_path for filter_path in filter_paths if check_conditions_in_path(condition_obj_paths, filter_path)]

def check_conditions_in_path(conditions, key_path):
    for condition in conditions:
        # print(f"condition is {condition}, key_path is {key_path}")
        if check_condition_in_path(condition, key_path):
            return 1
    return 0

def check_condition_in_path(condition, key_path):
    split_key_paths = split_list_at_str(key_path)
    split_conditions = split_list_at_str(condition)
    for split_condition in split_conditions:
        if not check_if_contain_by_split_path(split_condition, split_key_paths):
            return 0
    return 1


def check_if_contain_by_split_path(split_condition, split_key_paths):
    for split_key_path in split_key_paths:
        # print(f"split_condition is {split_condition}, split_key_path is {split_key_path}")
        if split_condition == split_key_path or (len(split_condition) == 1 and split_condition[0] in split_key_path):
            return 1
    return 0

def check_target_in_path(target, key_path):
    sort_targets = split_list_at_str(target)
    key_path_str = ','.join(map(str, key_path))
    print(f"key_path is {key_path}, key_path_str is {key_path_str}")
    for sort_target in sort_targets:
        sort_target_str = ','.join(map(str, sort_target))
        # print(f"sort_target_str is {sort_target_str}, key_path_str is {key_path_str}")
        if sort_target_str not in key_path_str:
            return 0
    return 1

def split_list_at_str(lst):
    result = []
    temp = []
    for item in lst:
        if isinstance(item, str):
            if temp:
                result.append(temp)
                temp = []
        temp.append(item)

    if temp:
        result.append(temp)

    return result

"""
get the subdata' obj and it's index, eg. [cells, 1] means cell 1
"""
def select_condition_path(obj, condition, condition_value, data):
    if 'small' in condition:
        value = int(condition_value[0])
        return [get_path(obj, subdata) for subdata in data if subdata[-1] < value and obj in subdata]
    elif 'big' in condition:
        value = int(condition_value[0])
        return [get_path(obj, subdata) for subdata in data if subdata[-1] > value and obj in subdata]
    elif 'range' in condition:
        start = int(condition_value[0])
        end = int(condition_value[1])
        return [get_path(obj, subdata) for subdata in data if start <= subdata[-1] <= end and obj in subdata]
    elif 'in' in condition and 'index' not in condition and 'notin' not in condition:
        values = [get_true_value(x) for x in condition_value]
        # print(f"values is {values} obj is {obj}")
        return [get_path(obj, subdata) for subdata in data if subdata[-1] in values and obj in subdata]
    elif 'index' in condition:
        print(f"condition_value is {condition_value} obj is {obj} data is {data}")
        if condition_value == 'all':
            return [(subdata[:-1] + [id]) for subdata in data for id in range(subdata[-1])]
        elif isinstance(condition_value, list):
            return [replace_last_list_data(subdata, int(x)) for x in condition_value for subdata in data if int(x) < subdata[-1]]
        else:
            return []
    elif 'new' in condition:
        value = int(condition_value[0])
        return [replace_last_list_data(subdata, id+subdata[-1]) for id in range(value) for subdata in data]
    elif 'notin' in condition:
        values = [get_true_value(x) for x in condition_value]
        # print(f"values is {values} obj is {obj}")
        return [get_path(obj, subdata) for subdata in data if subdata[-1] not in values and obj in subdata]

def get_true_value(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
            return value
        except json.JSONDecodeError:
            return value
    else:
        return value

def replace_last_list_data(list_data, replace_data):
    # print(f"list_data is {list_data}, replace_data is {replace_data}")
    new_list = list_data[:-1]
    new_list.append(replace_data)
    return new_list

def get_path(obj, subdata):
    if subdata[-2] == obj:
        return subdata[:subdata.index(obj)+1]
    else:
        return subdata[:subdata.index(obj)+2]

def prepare_find_key(find_key):
    if isinstance(find_key, list):
        if len(find_key) == 1:
            return find_key[0], 'all'
        elif len(find_key) == 2 and len(find_key[1]) > 0:
            return find_key[0], find_key[1]
        else:
            print(f"error find key {find_key}")
            return None, None
    else:
        return find_key, None

def get_key_path(find_key, data, sub_key, current_path_list = [], key_path = defaultdict(int), father_key=None):

    # find_key, index = prepare_find_key(find_key)

    if father_key is not None:
        current_path_list.append(father_key)

    if isinstance(data, list):
        for id, sub_data in enumerate(data):
            if len(current_path_list) > 0:
                level_path_list = current_path_list.copy()
                key_path = get_key_path(find_key, sub_data, sub_key, level_path_list, key_path, id)
    elif isinstance(data, dict):
        for k, v in data.items():
            level_path_list = current_path_list.copy()
            if k == find_key:
                register_path_list = level_path_list.copy()
                register_path_list.append(k)
                if k in key_path.keys():
                    key_path[k].append(register_path_list)
                else:
                    key_path[k] = [register_path_list]
            if sub_key is not None and k == sub_key:
                register_path_list = level_path_list.copy()
                register_path_list.append(k)
                if isinstance(v, list):
                    register_path_list.append(len(v))
                else:
                    register_path_list.append(v)
                register_k = k +'_obj'
                if register_k in key_path.keys():
                    key_path[register_k].append(register_path_list)
                else:
                    key_path[register_k] = [register_path_list]
            key_path = get_key_path(find_key, v, sub_key, level_path_list, key_path, k)
    else:
        pass

    return key_path

def check_k_in_obj(k, obj_infos):
    for obj_info in obj_infos:
        if obj_info['object'] == k:
            return 1
    return 0


def prepare_key_string(key_path):
    jsonpath_string = "$"
    for key in key_path:
        if isinstance(key, int):
            jsonpath_string += f"[{key}]"
        else:
            jsonpath_string += f".{key}"
    return jsonpath_string

def check_key_path(key_path, json_data):
    jsonpath_string = prepare_key_string(key_path)
    jsonpath_expr = parse(jsonpath_string)
    match = jsonpath_expr.find(json_data)
    is_valid = True if match else False
    return is_valid

def get_object_command(command, command_object):
    command_items = source_commands if command_object == 'source' else target_commands
    return tuple(command.get(key) for key in command_items)

def get_object_path(key, decorates, json_data, command_object):
    condition_paths = []
    for decorate in decorates:
        obj, obj_key, obj_condition, obj_condition_value = get_object_command(decorate, command_object)
        if obj is None:
            continue
        obj_key = obj if obj_key is None else obj_key
        key_paths = get_key_path(key, json_data, obj_key, [], {})
        print(f"decorate is {decorate}, obj is {obj} obj_key is {obj_key} obj_condition is {obj_condition} obj_condition_value is {obj_condition_value} key_paths is {key_paths}")
        if obj_condition is not None:
            obj_key += '_obj'
            #keep obj must in the key_paths[obj_key]
            print(f"key_paths[{obj_key}] is {key_paths[obj_key]}, conditions is {condition_paths}")
            key_paths[obj_key] = select_right_path(key_paths[obj_key], condition_paths)
            print(f"key_paths[{obj_key}] is {key_paths[obj_key]}, obj is {obj}, obj_condition is {obj_condition}, obj_condition_value is {obj_condition_value}")
            condition_path = select_condition_path(obj, obj_condition, obj_condition_value, key_paths[obj_key])
            print(f"condition_path is {condition_path}")
            condition_paths.append(condition_path)
            # just keep the last condition cause previous condition have been checked before
            condition_paths = condition_paths[-1:]
        else:
            condition_paths.append([[obj]])

    print(f"condition_paths is {condition_paths}")
    key_paths[key] = select_right_path(key_paths[key], condition_paths)
        # print(f"key_paths is {key_paths}")
    # if obj_condition is not None:
    #     key_paths[obj_key] = select_right_path(key_paths[obj_key], obj)
    #     condition_path = select_condition_path(key_paths, obj_key, key, obj_condition, obj_condition_value)
    #     # print(f"condition_path is {condition_path}, key_paths is {key_paths[key]}")
    #     key_paths[key] = select_right_path(key_paths[key], condition_path, 1)
    
    return key_paths[key]
