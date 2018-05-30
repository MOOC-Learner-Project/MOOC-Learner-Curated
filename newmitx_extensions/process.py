# /usr/bin/env python

import io
import os.path
import json
import csv
import datetime

typedict = {}


def report(anything, flag=True):
    global typedict
    if flag in typedict:
        typedict[flag] += 1
    else:
        typedict[flag] = 1


def get_fields(dicts):
    if not dicts:
        return []
    if not isinstance(dicts, list) \
            or not isinstance(dicts[0], dict):
        raise ValueError("Invalid dicts")
    fields = sorted(list(dicts[0].keys()))
    '''
    for d in dicts:
        if sorted(list(d.keys())) != fields:
            raise ValueError("Invalid dicts")
    '''
    return fields


def loading(dir_path, file_input):
    if not os.path.isdir(dir_path):
        raise ValueError("Invalid input path")
    dir_path = os.path.abspath(dir_path)
    return {_input: load_file(os.path.join(dir_path + '/' + file_input[_input]))
            for _input in file_input}


def load_file(path):
    with open(path, 'r') as json_file:
        json_lines = json_file.readlines()
        dicts = [json.loads(x) for x in json_lines]
    return dicts


def saving(dir_path, file_output, output_collection, output_fileds):
    if not os.path.isdir(dir_path):
        raise ValueError("Invalid input path")
    dir_path = os.path.abspath(dir_path)
    if not all(_output in output_collection for _output in file_output):
        raise ValueError("Insufficient output_dict")
    for _output in file_output:
        save_file(os.path.join(dir_path + '/' + file_output[_output]),
                  output_collection[_output],
                  output_fileds[_output])


def save_file(path, dicts, fields):
    save_csv(path, dicts, fields)


def save_csv(path, dicts, fields):
    if set(fields) != set(get_fields(dicts)):
        raise ValueError("Invaid output_fields")
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(
            csv_file,
            delimiter='\t' if path.endswith('.sql')
            else ',',
            fieldnames=fields,
            quotechar='"',
            escapechar='\\',
            lineterminator='\n')
        for d in dicts:
            writer.writerow({f: (d[f].encode('utf-8')
                             if isinstance(d[f], unicode)
                             else d[f])
                             if f in d
                             else None
                             for f in fields})


def mapping(input_collection, map_dict):
    return {_output: [map_unit(
        map_obj[0],
        input_collection[map_obj[1]],
        map_obj[2]
    )
        for map_obj in map_dict[_output]]
        for _output in map_dict}


def map_unit(order, dicts, unit_map):
    if order == (0, 0):
        return map_unit_0_0(dicts, unit_map)
    elif order == (0, 1):
        return map_unit_0_1(dicts, unit_map)
    elif order == (0, 2):
        return map_unit_0_2(dicts, unit_map)
    elif order == (2, 2):
        return map_unit_2_2(dicts, unit_map)
    else:
        raise ValueError("Invalid map order")


def map_unit_0_0(dicts, unit_map):
    return [{f: d[unit_map[f]] if unit_map[f] in d else report(d, unit_map[f])
             for f in unit_map}
            for d in dicts]


def map_unit_0_1(dicts, unit_map):
    return [{f: unit_map[f](d)
             for f in unit_map}
            for d in dicts]


def map_unit_0_2(dicts, unit_map):
    return [{f: unit_map[f](d, dicts)
             for f in unit_map}
            for d in dicts]


def map_unit_2_2(dicts, unit_map):
    return unit_map(dicts)


def concatenating(mapped_collection):
    return {_output: concat_dicts(mapped_collection[_output])
            for _output in mapped_collection}


def all_disjoint(sets):
    union = set()
    for s in sets:
        for x in s:
            if x in union:
                return False
            union.add(x)
    return True


def concat_dict(list_of_dict):
    if not all(isinstance(d, dict) for d in list_of_dict):
        raise ValueError("Invalid list_of_dict")
    if not all_disjoint([set(d.keys()) for d in list_of_dict]):
        raise ValueError("Illegal concatenation of list_of_dict")
    sd = {}
    for d in list_of_dict:
        sd.update(d)
    return sd


def concat_dicts(list_of_dicts):
    if not list_of_dicts:
        return []
    if not all(len(dicts) == len(list_of_dicts[0])
               for dicts in list_of_dicts):
        raise ValueError("Illegal concatenation of list_of_dicts")
    return [concat_dict([list_of_dicts[x][y]
                         for x in range(len(list_of_dicts))])
            for y in range(len(list_of_dicts[0]))]