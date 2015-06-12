#!/usr/bin/env python

import json
import sys

packages_file = open(sys.argv[1], 'r')
list_pkg = json.load(packages_file)

dict_pkg = {}

for i in range(len(list_pkg)):
    def_pkg = dict([(list_pkg[i].get('name'), list_pkg[i]['requires'])])
    dict_pkg.update(def_pkg)


def wrapper_dep(root, dict):
    root_dep = dict.pop(root)
    for dep in root_dep:
        if dict[dep] == []:
            print(dep)
        else:
            wrapper_dep(dep, dict)
    print(root)


wrapper_dep(sys.argv[2], dict_pkg)
