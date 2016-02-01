#!/usr/bin/python3

import itertools
import sys
import yaml

from pydoc import locate

                    ########################################

def print_errors(prefix, err_list, err_num, err_msg):

    for item in err_list:
        print("Error(%2.2X): %s/%s %s" % (err_num, prefix, item, err_msg))

                    ########################################
                    ########################################

# Init specifications of the YAML files (in YAML too, yes!)
yaml_ctrl_specs = """\
%YAML 1.2
---

fields:
    object:
        presence: mandatory
        type: str
        values: [scalar, array, varying_array]
    object_dims:
        presence:
            scalar: optional
            array: mandatory
            varying_array: mandatory
        type: list
        values: ["#number", "@ref"]
    type:
        presence: mandatory
        type: str
        values: [char, double, float, int, long_int, short_int, unsigned_int]
    values:
        presence: optional
        type: list
    range:
        presence: optional
        type: list
        values: ["#range"]

"""
yaml_ctrl = yaml.load(yaml_ctrl_specs)

with open("escdf-geometry-specs-0.1.yml", "r") as yaml_doc:
    yaml_data = yaml.load(yaml_doc)

                    ########################################

# Init list of fields (will be modified later on each error encountered)
data_fields = [field for field in yaml_data["metadata"]]

                    ########################################

# Check that all fields are defined
data_undefined = [item for item in data_fields \
    if yaml_data["metadata"][item] is None]
if ( len(data_undefined) > 0 ):
    print_errors("/metadata", data_undefined, 0x1, "is empty")
    data_fields = [item for item in data_fields if not item in data_undefined]

                    ########################################

# Check presence of mandatory fields
ctrl_mandatory = [item for item in yaml_ctrl["fields"] \
    if yaml_ctrl["fields"][item]["presence"] == "mandatory"]
data_missing = [["%s/%s" % (field, item) for field in data_fields \
    if not item in yaml_data["metadata"][field]] \
    for item in ctrl_mandatory]
data_missing = list(itertools.chain.from_iterable(data_missing))
if ( len(data_missing) > 0 ):
    print_errors("/metadata", data_missing, 0x2, "is missing")
    data_fields = [item for item in data_fields if not item in data_missing]

# TODO: object_dims presence depends on object type

                    ########################################

# Check absence of undeclared fields
data_unknown = [["%s/%s" % (field, item) \
    for item in yaml_data["metadata"][field].keys() \
    if not item in yaml_ctrl["fields"]] \
    for field in data_fields]
data_unknown = list(itertools.chain.from_iterable(data_unknown))
if ( len(data_unknown) > 0 ):
    print_errors("/metadata", data_unknown, 0x3, "is not a field")
    data_fields = [item for item in data_fields if not item in data_unknown]

                    ########################################

# Check field types
data_wrongtype = []
for field in data_fields:
    for item in yaml_data["metadata"][field]:
        expected_type = yaml_ctrl["fields"][item]["type"]
        if ( not isinstance(yaml_data["metadata"][field][item],
             locate(yaml_ctrl["fields"][item]["type"])) ):
            data_wrongtype.append("%s/%s<%s>" % (field, item, expected_type))
if ( len(data_wrongtype) > 0 ):
    print_errors("/metadata", data_wrongtype, 0x4, "has a wrong type")
    data_fields = [item for item in data_fields if not item in data_wrongtype]

                    ########################################

# Check that strings are the only scalars with a dimension
data_scalars = [item for item in data_fields \
    if yaml_data["metadata"][item]["object"] == "scalar"]
data_wrongdims = [item for item in data_scalars \
    if ( ("object_dims" in yaml_data["metadata"][item]) and \
         (not yaml_data["metadata"][item]["type"] == "char" ) )]
if ( len(data_wrongdims) > 0 ):
    print_errors("/metadata", data_wrongdims, 0x5, "cannot have a dimension")
    data_fields = [item for item in data_fields if not item in data_wrongdims]

                    ########################################

# Check field values
data_wrong = []
data_refs = []
for field in data_fields:
    for item in yaml_ctrl["fields"].keys():
        try:
            raw_value = yaml_data["metadata"][field][item]
            if ( not isinstance(raw_value, (list, set)) ):
                raw_value = [raw_value]
            raw_allow = yaml_ctrl["fields"][item]["values"]
        except KeyError:
            raw_value = []
            raw_allow = []
        for fnd_value in raw_value:
            fnd_value_ok = False
            for fnd_allow in raw_allow:
                if ( fnd_allow[0] == "#" ):
                    if ( fnd_allow == "#number" ):
                        if ( isinstance(fnd_value, int) ):
                            fnd_value_ok = True
                            break
                    elif ( fnd_allow == "#range" ):
                        if ( isinstance(fnd_value, int) and \
                             (len(raw_value) == 2) ):
                            fnd_value_ok = True
                            break
                    else:
                        raise NotImplementedError("no test for %s" % fnd_allow)
                elif ( fnd_allow == "@ref" ):
                    if ( fnd_value[0] == "@" ):
                        data_refs.append((field, fnd_value[1:]))
                        fnd_value_ok = True
                        break
                else:
                    if ( fnd_allow == fnd_value ):
                        fnd_value_ok = True
                        break
            if ( not fnd_value_ok ):
                data_wrong.append("%s/%s = %s" % (field, item, fnd_value))
if ( len(data_wrong) > 0 ):
    print_errors("/metadata", data_wrong, 0x10, "is forbidden")
    data_fields = [item for item in data_fields if not item in data_wrong]

                    ########################################

# Check references to other fields in object dimensions
data_objdims = [[field, yaml_data["metadata"][field]["object_dims"]] \
    for field in data_fields if "object_dims" in yaml_data["metadata"][field]]
data_reffixed = {}
data_refvarying = {}
data_brokenrefs = []
for dim_info in data_objdims:
    field = dim_info[0]
    dims = dim_info[1]
    if ( not isinstance(dims, list) ):
        dims = [dims]
    for item in dims:
        item = str(item)
        if ( item[0] == "@" ):
            if (  (not item[1:] in data_fields) and \
                  (not item[1:-3] in data_fields) ):
                data_brokenrefs.append("%s[%s]" % (field, item))
                continue
            if ( item[-3:] == "(?)" ):
                if ( not field in data_refvarying ):
                    data_refvarying[field] = []
                data_refvarying[field].append(item[1:-3])
            else:
                if ( not field in data_reffixed ):
                    data_reffixed[field] = []
                data_reffixed[field].append(item[1:])
if ( len(data_brokenrefs) > 0 ):
    print_errors("/metadata", data_brokenrefs, 0x11, "reference is dangling")
    data_fields = [item for item in data_fields if not item in data_brokenrefs]

# Check that fixed-length reference targets are scalars
data_wrongreffixed = []
for field in data_reffixed:
    for dim in data_reffixed[field]:
        if ( yaml_data["metadata"][dim]["object"] != "scalar" ):
            data_wrongreffixed.append("%s[@%s]" % (field, dim))
if ( len(data_wrongreffixed) > 0 ):
    print_errors("/metadata", data_wrongreffixed, 0x12, "reference must point to a scalar")
    data_fields = [item for item in data_fields if not item in data_wrongreffixed]

# Check that varying-length reference targets are vectors
data_wrongrefvarying = []
for field in data_refvarying:
    for dim in data_refvarying[field]:
        if ( (yaml_data["metadata"][dim]["object"] != "array") or \
             (len(yaml_data["metadata"][dim]["object_dims"]) != 1) ):
            data_wrongrefvarying.append("%s[@%s(?)]" % (field, dim))
if ( len(data_wrongrefvarying) > 0 ):
    print_errors("/metadata", data_wrongrefvarying, 0x12, "reference must point to a vector")
    data_fields = [item for item in data_fields if not item in data_wrongrefvarying]

                    ########################################
                    ########################################

# Everything OK: generate dependency tree

