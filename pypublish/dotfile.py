import yaml
import os

PYPUBLISH = "pypublish"


def read(filename):
    if not os.path.exists(filename):
        return dict()

    stream = file(filename, "r")
    document = yaml.load(stream)
    if PYPUBLISH not in document.keys():
        print "Error : file %s does not define the 'pypublish' entry point" % filename
        exit(-1)
    root = document.get(PYPUBLISH)
    return read_node(root, "", dict())


def read_node(node, prefix, options):
    for key in node.keys():
        value = node.get(key)
        newkey = "%s.%s" % (prefix, key)
        if newkey.startswith("."):
            newkey = newkey[1:]
        if type(value) is dict:
            read_node(value, "%s.%s" % (prefix, key), options)
        elif type(value) is str:
            options[newkey] = value
        elif type(value) is bool:
            options[newkey] = bool(value)
        else:
            print "unknown type %s" % type(value)
            exit(-1)
    return options


