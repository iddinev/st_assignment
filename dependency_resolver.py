#!/usr/bin/env python

import json
import sys

packages_file = open(sys.argv[1], 'r')
list_pkg = json.load(packages_file)

dict_pkg = {}
for i in range(len(list_pkg)):
    def_pkg = dict([(list_pkg[i].get('name'), list_pkg[i]['requires'])])
    dict_pkg.update(def_pkg)
