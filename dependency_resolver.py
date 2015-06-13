#!/usr/bin/env python


from json import load
from sys import argv
from collections import OrderedDict


try:

    with open(argv[1], 'r') as packages_file:
        list_pkg = load(packages_file)
        if isinstance(list_pkg, list) is False:
            raise TypeError

except ValueError as err:
    print("ERR: Erroneous JSON data :", err)
    exit(1)
except TypeError:
    print("ERR: JSON data expected in an array not object containing array")
    exit(1)
except IOError as err:
    print("ERR: File read error :", err)
    exit(1)


# Make simple {'name': '[deps]'} dict from input list of dicts for easier use
dict_pkg = {}
try:

    for i in range(len(list_pkg)):

            if 'name' not in list_pkg[i] or 'requires' not in list_pkg[i]:
                raise KeyError
            elif isinstance(list_pkg[i]['name'], str) is False:
                raise NameError
            elif isinstance(list_pkg[i]['requires'], list) is False:
                raise TypeError

            def_pkg = dict([(list_pkg[i].get('name'), list_pkg[i]['requires'])])
            dict_pkg.update(def_pkg)

except (KeyError, NameError, TypeError):
    print('ERR: Definitions must be {"name" : "pkg_name", "requires" : ["deps"]}')
    exit(1)


# Actuall function that resolves the order of the packages
ordered_list = []
def dep_resolver(root, dict, list):

    root_dep = dict.pop(root)

    try:

        for dep in root_dep:
            if isinstance(dep, str) is False:
                raise TypeError(root, dep)
            elif dict[dep] == []:
                list.append(dep)
            else:
                dep_resolver(dep, dict, list)
        list.append(root)

    except TypeError as err:
        print("ERR: Dependency", err.args[1], "of package", err.args[0], "not a string")
        exit(1)
    except KeyError as err:
        print("ERR: Missing dependency definition for package", err)
        exit(1)


dep_resolver(argv[2], dict_pkg, ordered_list)
# Remove duplicate dependencies
resolved_list = list(OrderedDict.fromkeys(ordered_list))
print(resolved_list)
